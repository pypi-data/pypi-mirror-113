#$Id$#

from books.model.BankRule import BankRule
from books.model.BankRuleList import BankRuleList
from books.model.Criteria import Criteria

class BankRulesParser:
    """This class is used to parse the json response for Bank rules."""
  
    def get_rules(self, resp):
        """This method parses the given response and returns list of bank 
            rules object.

        Args:
            resp(dict): Dictionary containing json object for bank rules.

        Returns:
            list of instance: List of Bank rules object.

        """
        bank_rules = BankRuleList()
        for value in resp['rules']:
            bank_rule = BankRule()
            bank_rule.set_rule_id(value['rule_id'])
            bank_rule.set_rule_name(value['rule_name'])
            bank_rule.set_rule_order(value['rule_order'])
            bank_rule.set_apply_to(value['apply_to'])
            bank_rule.set_criteria_type(value['criteria_type'])
            bank_rule.set_record_as(value['record_as'])
            bank_rule.set_account_id(value['account_id'])
            bank_rule.set_account_name(value['account_name'])
            for criteria_value in value['criterion']:
                criteria = Criteria()
                criteria.set_criteria_id(criteria_value['criteria_id'])
                criteria.set_field(criteria_value['field'])
                criteria.set_comparator(criteria_value['comparator'])
                criteria.set_value(criteria_value['value'])
                bank_rule.set_criterion(criteria)
            bank_rules.set_bank_rules(bank_rule)
        return bank_rules

    def get_rule(self, resp):
        """This method parses the given response and returns bank rule object.

        Args:
            resp(dict): Dictionary containing json object for bank rules.

        Returns:  
            instance: Bank rules object.

        """
        bank_rule = BankRule()
        rule = resp['rule']
        bank_rule.set_rule_id(rule['rule_id'])
        bank_rule.set_rule_name(rule['rule_name'])
        bank_rule.set_rule_order(rule['rule_order'])
        bank_rule.set_apply_to(rule['apply_to'])
        bank_rule.set_criteria_type(rule['criteria_type'])
        bank_rule.set_record_as(rule['record_as'])
        for value in rule['criterion']:
            criteria = Criteria()
            criteria.set_criteria_id(value['criteria_id'])  
            criteria.set_field(value['field'])
            criteria.set_comparator(value['comparator'])
            criteria.set_value(value['value'])
            bank_rule.set_criterion(criteria)
        bank_rule.set_account_id(rule['account_id'])
        bank_rule.set_account_name(rule['account_name'])
        bank_rule.set_tax_id(rule['tax_id'])
        bank_rule.set_customer_id(rule['customer_id'])
        bank_rule.set_customer_name(rule['customer_name'])
        bank_rule.set_reference_number(rule['reference_number'])
        return bank_rule

    def get_message(self, resp):
        """This method parses the given response and returns message string.

        Args:
            resp(dict): Dictionary containing json object for message.

        Returns: 
            str: Success message.

        """
        return resp['message']

