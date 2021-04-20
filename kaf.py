#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys

import re
import json
import Ice

Ice.loadSlice('-I /usr/share/slice /usr/share/slice/dharma/scone-wrapper.ice --all')
import Semantic


class AbstractRule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, AbstractRule):
            return False

        return (self.left, self.right) == (other.left, other.right)

    def __repr__(self):
        return "AbstractRule:\n{}\n=>\n{}".format(self.left, self.right)


class AbstractRuleBuilder:
    def __init__(self, scone, scenario):
        self.scone = scone
        self.scenario = scenario
        self.build()

    def build(self):
        with open(self.scenario) as json_file:
            rooms = json.load(json_file)

        self.requirements = self.get_relations('require')
        self.implications = self.get_relations('indicate')
        self.rules = []

        for room in rooms:
            self.build_room(room)

        [print('----\n{}'.format(rule)) for rule in self.rules]

    def build_room(self, room):
        for device in room['devices']:
            for provision in self.get_provisions(device['type']):
                if self.is_sensor(device):
                    self.build_sensor(room, provision, device)
                else:
                    self.build_actuator(room, provision, device)

    def build_sensor(self, room, provision, device):
        lhs = [{
            'agent': device['id'],
            'value': provision['resource']
        }]

        rhs = []
        for implication in self.filter_rels(self.implications, 'a', provision['resource']):
            rhs.append({
                'location': room['name'],
                'value': implication['b']
            })

            self.rules.append(AbstractRule(lhs, rhs))

    def build_actuator(self, room, provision, device):
        rhs = [{
            'action': 'provide {}'.format(provision['resource']),
            'object': device['id']
        }]

        lhs = []
        for requeriment in self.filter_rels(self.requirements, 'b', provision['resource']):
            lhs = [{
                'location': room['name'],
                'value': requeriment['a']
            }]

            if room['natural light'] == True:
                lhs.append({
                    'time': 'night'
                })

            self.rules.append(AbstractRule(lhs, rhs))

    def is_sensor(self, device):
        request = '(is-x-a-y? {%s}{sensor})' % (device['type'])
        reply = self.scone.request(request)
        return reply == 'YES'

    def get_provisions(self, provider):
        request = '(list-all-x-inverse-of-y {provider}{%s})' % (provider)
        reply = self.scone.request(request)
        resources = self.parse_entities(reply)
        provisions = []

        for resource in resources:
            provision = {
                'provider': provider,
                'resource': resource,
            }

            provisions.append(provision)

        return provisions

    def filter_rels(self, relations, link_element, entity_name):
        return [r for r in relations if r[link_element] == entity_name]

    def parse_entities(self, scone_reply):
        return re.findall(r'{(.*?)}', scone_reply)

    def get_instances(self, instance_type):
        request = '(list-instances {%s})' % (instance_type)
        reply = self.scone.request(request)

        return self.parse_entities(reply)

    def get_rel_element(self, link_element, relation):
        request = '(%s-element {%s})' % (link_element, relation)
        reply = self.scone.request(request)

        return self.parse_entities(reply)[0]

    def get_relations(self, relation_name):
        relation_ids = self.get_instances(relation_name)
        relations = []

        for relation_id in relation_ids:
            relation = {
                'id': relation_id,
                'a': self.get_rel_element('a', relation_id),
                'b': self.get_rel_element('b', relation_id)
            }

            relations.append(relation)

        return relations


class KAF_Client(Ice.Application):
    def run(self, argv):
        self.ic = self.communicator()
        scone = self.scone_service()
        AbstractRuleBuilder(scone, argv[1])

    def scone_service(self):
        proxy = self.ic.propertyToProxy('Scone.Proxy')
        scone = Semantic.SconeServicePrx.checkedCast(proxy)

        if not scone:
            raise RuntimeError('Invalid proxy')

        return scone


if __name__ == '__main__':
    sys.exit(KAF_Client().main(sys.argv))
