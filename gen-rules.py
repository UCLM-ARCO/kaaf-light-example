#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys

import re
import json
import Ice

Ice.loadSlice('-I /usr/share/slice /usr/share/slice/dharma/scone-wrapper.ice --all')
import Semantic


class RuleGenerator(Ice.Application):
    def run(self, argv):
        self.ic = self.communicator()
        self.scone = self.scone_service()

        with open(argv[1]) as json_file:
            rooms = json.load(json_file)

        # ---------

        # requirements = self.get_relations('require')
        # provisions = self.get_relations('provide')
        # rules = []

        # for room in scene['rooms']:
        #     for requirement in requirements:
        #         for provision in self.filter_rels(provisions, 'b', requirement['b']):
        #             rule = self.gen_rule(room['name'], requirement['a'], provision['a'])
        #             rules.append(rule)

        # [print('{}\n'.format(rule)) for rule in rules]

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
        lhs = '{} from {}'.format(provision['resource'], device['id'])
        for implication in self.filter_rels(self.implications, 'a', provision['resource']):
            rhs = '{}: {}'.format(room['name'], implication['b'])
            self.rules.append('{}\n=>\n{}'.format(lhs, rhs))

    def build_actuator(self, room, provision, device):
        rhs = 'provide {} with {}'.format(provision['resource'], device['id'])
        for requeriment in self.filter_rels(self.requirements, 'b', provision['resource']):
            lhs = '{}: {}'.format(room['name'], requeriment['a'])
            self.rules.append('{}\n=>\n{}'.format(lhs, rhs))

    def is_sensor(self, device):
        request = '(is-x-a-y? {%s}{sensor})' % (device['type'])
        reply = self.scone.request(request)
        return reply == 'YES'

    def gen_rule(self, room, pre, action):
        protasis = '{}: {}'.format(room, pre)     # part of the LHS
        apodasis = '{}: {}'.format(room, action)  # part of the RHS
        return '{}\n=>\n{}'.format(protasis, apodasis)
    
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

    def scone_service(self):
        proxy = self.ic.propertyToProxy('Scone.Proxy')
        scone = Semantic.SconeServicePrx.checkedCast(proxy)

        if not scone:
            raise RuntimeError('Invalid proxy')

        return scone


sys.exit(RuleGenerator().main(sys.argv))
