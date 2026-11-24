"""Offline atlas integrity and cross-site scripting regression tests.
Author: Komorebi P.
"""
import unittest
from render_sequence_variable_horizon_atlas import render


class TestAtlas(unittest.TestCase):
    def test_exact_replay_counts(self):
        r={'indexed_formula_hyperedges':2,'query_plans_with_selected_indexed_edge':1,
           'query_plan_values_checked':42,
           'indexed_edge_detail':[
             {'target':'A000045','inputs':['A000012'],'rhs':'A000012(2*n)',
              'index_maps':{'A000012':[[2,0]]},'required_input_horizons':{'A000012':40},
              'score':20,'independent_direct_score':45,'source_text_sha256':'ab',
              'cost_model_choice':'indexed_transfer'},
             {'target':'A000108','inputs':['A000984'],'rhs':'A000984(n)/(n+1)',
              'index_maps':{'A000984':[[1,0]]},'required_input_horizons':{'A000984':20},
              'score':60,'independent_direct_score':50,'source_text_sha256':'cd',
              'cost_model_choice':'direct'},
           ]}
        page=render(r)
        self.assertIn('2</strong>',page)
        self.assertIn('42</strong>',page)
        self.assertIn('JSON.parse',page)
        self.assertIn('textContent',page)

    def test_untrusted_source_formula_is_not_injected_as_html(self):
        attack='</script><img src=x onerror=alert(1)>'
        r={'indexed_formula_hyperedges':1,'query_plans_with_selected_indexed_edge':0,
           'query_plan_values_checked':0,'indexed_edge_detail':[
             {'target':'A123456','inputs':[],'rhs':attack,'index_maps':{},
              'required_input_horizons':{},'score':1,'independent_direct_score':1,
              'source_text_sha256':'x','cost_model_choice':'direct'}]}
        page=render(r)
        self.assertNotIn(attack,page)
        self.assertIn('\\u003c/script\\u003e',page)

    def test_mismatched_provenance_counts_rejected(self):
        with self.assertRaises(ValueError):
            render({'indexed_formula_hyperedges':2,'query_plans_with_selected_indexed_edge':0,
                    'indexed_edge_detail':[],'query_plan_values_checked':0})

if __name__=='__main__':unittest.main()
