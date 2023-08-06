import re
from inspect import signature
from typing import Any, Dict, Optional
from .factory import Strategy, Factory, Config


class Injectark:
    def __init__(self, factory: Factory = None,
                 strategy: Strategy = None,
                 parent: 'Injectark' = None) -> None:
        self.parent = parent
        self.factory = factory
        self.strategy = strategy or {}
        self.registry: Dict[str, Any] = {}
        self.pattern = re.compile(r'(?<!^)(?=[A-Z])')

    @property
    def config(self) -> Config:
        return getattr(self.factory, 'config', {})

    def __getitem__(self, key: str):
        public = getattr(self.factory, 'public', [])
        if public and key not in public:
            raise KeyError(
                f"No public access for resource '{key}'.")

        return self.resolve(key, strict=True)

    def resolve(self, resource: str, strict: bool = False):
        fetched = self._registry_fetch(resource)
        if fetched:
            return fetched

        persist = not self.strategy.get(resource, {}).get('ephemeral', False)
        instance = self._dependency_build(resource, persist)

        if strict and not instance:
            raise KeyError(
                f"The '{resource}' resource could not be resolved.")

        return instance

    def forge(self, factory, strategy):
        return Injectark(parent=self, strategy=strategy, factory=factory)

    def _registry_fetch(self, resource: str):
        fetched = False
        rule = self.strategy.get(resource, {})
        if rule.get('unique'):
            return fetched

        if resource in self.registry:
            fetched = self.registry[resource]
        else:
            parent = self.parent
            fetched = parent._registry_fetch(resource) if parent else False

        return fetched

    def _dependency_build(self, resource: str, persist=True):
        instance = None
        rule = self.strategy.get(resource, {'method': ''})
        method = rule['method'] or self.pattern.sub('_', resource).lower()
        builder = self.factory.extract(method)

        if builder:
            dependencies = [
                value.annotation.__name__ for key, value in
                signature(builder).parameters.items() if key != 'return']

            dependency_instances = []
            for dependency in dependencies:
                dependency_instance = self.resolve(dependency, strict=True)
                dependency_instances.append(dependency_instance)

            instance = builder(*dependency_instances)

        else:
            instance = (self.parent._dependency_build(resource, persist)
                        if self.parent else instance)

            persist = (persist and self.strategy.get(
                resource, {}).get('unique', False))

        if persist:
            self.registry[resource] = instance

        return instance
