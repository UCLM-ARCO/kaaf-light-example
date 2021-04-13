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
            scene = json.load(json_file)

        requirements = self.get_relations('require')
        provisions = self.get_relations('provide')
        rules = []

        for requirement in requirements:
            for room in scene['rooms']:
                for provision in self.filter_rels(provisions, 'b', requirement['b']):
                    rule = self.gen_rule(room['name'], requirement['a'], provision['a'])
                    rules.append(rule)
        
        [print('{}\n'.format(rule)) for rule in rules]

    def gen_rule(self, room, pre, action):
        protasis = '{}: {}'.format(room, pre)     # part of the LHS
        apodasis = '{}: {}'.format(room, action)  # part of the RHS
        return '{}\n=>\n{}'.format(protasis, apodasis)

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