import logging
import time
import urllib.parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

import requests

from src import Core
from src.lib import snow_maps


class SnowDataHelper:
    """
    Helper class to interact with ServiceNow data.
    """

    def __init__(self, sn_user: str, sn_pass: str, sn_host: str, log_level: int):
        """
        Initialize the SnowDataHelper instance.

        :param sn_user: ServiceNow username
        :param sn_pass: ServiceNow password
        :param sn_host: ServiceNow host URL
        :param log_level: Logging level
        """
        self.sn_user = sn_user
        self.sn_pass = sn_pass
        self.sn_host = sn_host
        self.logger = logging.getLogger("SnowDataHelper")
        self.logger.setLevel(log_level)
        self.logger.propagate = False

    def __query_snow_data(self, url: str) -> tuple:
        """
        Query data from ServiceNow.

        :param url: URL to query
        :return: Tuple containing the response data and the query time
        """
        start_ts = time.time()
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, auth=(self.sn_user, self.sn_pass), headers=headers)
        response.raise_for_status()
        data = response.json()
        end_query_ts = time.time()
        total_time = end_query_ts - start_ts
        return data, total_time

    def get_sc_task_data(self, sys_id: str) -> dict:
        """
        Get ServiceNow task data by sys_id.

        :param sys_id: Task sys_id
        :return: Task data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_task/{sys_id}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_task sys_id: {sys_id}, query_time: {total_time}")
        return data["result"]

    def get_sc_task_data_by_effective_number(self, task_effective_number: str) -> dict:
        """
        Get ServiceNow task data by effective number.

        :param task_effective_number: Task effective number
        :return: Task data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_task?sysparm_query=task_effective_number={task_effective_number}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_task sys_id: {task_effective_number}, query_time: {total_time}")
        return data["result"]

    def get_sc_req_item_data(self, sys_id: str) -> dict:
        """
        Get ServiceNow request item data by sys_id.

        :param sys_id: Request item sys_id
        :return: Request item data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_req_item/{sys_id}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_req_item sys_id: {sys_id}, query_time: {total_time}")
        return data["result"]

    def get_sc_req_item_data_by_effective_number(self, task_effective_number: str) -> dict:
        """
        Get ServiceNow request item data by effective number.

        :param task_effective_number: Request item effective number
        :return: Request item data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_req_item?sysparm_query=task_effective_number={task_effective_number}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_req_item sys_id: {task_effective_number}, query_time: {total_time}")
        return data["result"]

    def get_sc_request_data(self, sys_id: str) -> dict:
        """
        Get ServiceNow request data by sys_id.

        :param sys_id: Request sys_id
        :return: Request data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_request/{sys_id}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_request sys_id: {sys_id}, query_time: {total_time}")
        return data["result"]

    def get_sc_request_data_by_effective_number(self, task_effective_number: str) -> dict:
        """
        Get ServiceNow request data by effective number.

        :param task_effective_number: Request effective number
        :return: Request data
        """
        url = f"https://{self.sn_host}/api/now/table/sc_request?sysparm_query=task_effective_number={task_effective_number}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"sc_request task_effective_number: {task_effective_number}, query_time: {total_time}")
        return data["result"]

    def get_incident_data(self, sys_id: str) -> dict:
        """
        Get ServiceNow incident data by sys_id.

        :param sys_id: Incident sys_id
        :return: Incident data
        """
        url = f"https://{self.sn_host}/api/now/table/incident/{sys_id}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"incident sys_id: {sys_id}, query_time: {total_time}")
        return data["result"]

    def get_incident_data_by_effective_number(self, task_effective_number: str) -> dict:
        """
        Get ServiceNow incident data by effective number.

        :param task_effective_number: Incident effective number
        :return: Incident data
        """
        url = f"https://{self.sn_host}/api/now/table/incident?sysparm_query=task_effective_number={task_effective_number}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"incident task_effective_number: {task_effective_number}, query_time: {total_time}")
        return data["result"]

    def get_change_request_data(self, sys_id: str) -> dict:
        """
        Get ServiceNow change request data by sys_id.

        :param sys_id: Change request sys_id
        :return: Change request data
        """
        url = f"https://{self.sn_host}/api/now/table/change_request/{sys_id}"
        data, total_time = self.__query_snow_data(url)
        self.logger.info(f"change_request sys_id: {sys_id}, query_time: {total_time}")
        return data["result"]

    @staticmethod
    def parse_snow_url(url: str) -> dict:
        """
        Parse a ServiceNow URL to extract table and sys_id.

        :param url: ServiceNow URL
        :return: Dictionary containing table and sys_id
        :raises ValueError: If sys_id is not found in the URL
        """
        unquote_url = urllib.parse.unquote(url)
        parsed_url = urlparse(unquote_url)
        captured_value = parse_qs(parsed_url.query)
        table = parsed_url.path.split("/").pop()
        if "sys_id" not in captured_value:
            raise ValueError("sys_id not found in the url")
        out = {"table": table, "sys_id": captured_value["sys_id"][0]}
        return out

    def build_snow_url(self, table: str, sys_id: str) -> str:
        """
        Build a ServiceNow URL for a given table and sys_id.

        :param table: ServiceNow table name
        :param sys_id: sys_id of the record
        :return: ServiceNow URL
        """
        out = urllib.parse.quote(f"{self.sn_host}/now/nav/ui/classic/params/target/{table}?sys_id={sys_id}",
                                 safe='/', encoding=None, errors=None)
        return f"https://{out}"

    def get_data_for_sc_task(self, sys_id: str) -> dict:
        """
        Get unified data for a ServiceNow task.

        :param sys_id: Task sys_id
        :return: Unified task data
        """
        task_data = Core.sdh.get_sc_task_data(sys_id=sys_id)
        if "request_item" in task_data:
            request_item_data = Core.sdh.get_sc_req_item_data(sys_id=task_data["request_item"]["value"])
        else:
            request_item_data = None
        return self.unify_data_for__sc_task(task_data, request_item_data)

    def get_data_for_sc_req_item(self, sys_id: str) -> dict:
        """
        Get unified data for a ServiceNow request item.

        :param sys_id: Request item sys_id
        :return: Unified request item data
        """
        _data = Core.sdh.get_sc_req_item_data(sys_id=sys_id)
        return self.unify_data_for__sc_req_item(_data)

    def get_data_for_sc_request(self, sys_id: str) -> dict:
        """
        Get unified data for a ServiceNow request.

        :param sys_id: Request sys_id
        :return: Unified request data
        """
        _data = Core.sdh.get_sc_request_data(sys_id=sys_id)
        return self.unify_data_for__sc_req_item(_data)

    def get_data_for_incident(self, sys_id: str) -> dict:
        """
        Get unified data for a ServiceNow incident.

        :param sys_id: Incident sys_id
        :return: Unified incident data
        """
        _data = Core.sdh.get_incident_data(sys_id=sys_id)
        return self.unify_data_for__incident(_data)

    def get_data_for_change_request(self, sys_id: str) -> dict:
        """
        Get unified data for a ServiceNow change request.

        :param sys_id: Change request sys_id
        :return: Unified change request data
        """
        _data = Core.sdh.get_change_request_data(sys_id=sys_id)
        return self.unify_data_for__change_request(_data)

    @staticmethod
    def unify_data_for__sc_req_item(item_data: dict) -> dict:
        """
        Unify data for a ServiceNow request item.

        :param item_data: Request item data
        :return: Unified request item data
        """
        out_data = {
            "task_effective_number": item_data[
                'task_effective_number'] if "task_effective_number" in item_data else "N/A",
            "short_description": item_data[
                'short_description'] if "short_description" in item_data else "N/A",
            "sys_created_on": item_data['sys_created_on'] if "sys_created_on" in item_data else "N/A",
            "priority": item_data['priority'] if "priority" in item_data else "N/A",
            "sys_updated_by": item_data['sys_updated_by'] if "sys_updated_by" in item_data else "N/A",
            "approval": item_data['approval'] if "approval" in item_data else "N/A",
            "state": snow_maps.sc_task_state_map[item_data['state']] if "state" in item_data else "N/A",
            "sys_created_by": item_data['sys_created_by'] if "sys_created_by" in item_data else "N/A",
            "target_link": Core.sdh.build_snow_url(table=f"{item_data['sys_class_name']}.do",
                                                   sys_id=item_data["sys_id"]),
            "sys_updated_on": item_data['sys_updated_on'] if "sys_updated_on" in item_data else "N/A",

        }
        return out_data

    @staticmethod
    def unify_data_for__incident(item_data: dict) -> dict:
        """
        Unify data for a ServiceNow incident.

        :param item_data: Incident data
        :return: Unified incident data
        """
        out_data = {
            "task_effective_number": item_data[
                'task_effective_number'] if "task_effective_number" in item_data else "N/A",
            "short_description": item_data[
                'short_description'] if "short_description" in item_data else "N/A",
            "sys_created_on": item_data['sys_created_on'] if "sys_created_on" in item_data else "N/A",
            "priority": item_data['priority'] if "priority" in item_data else "N/A",
            "sys_updated_by": item_data['sys_updated_by'] if "sys_updated_by" in item_data else "N/A",
            "approval": item_data['approval'] if "approval" in item_data else "N/A",
            "state": snow_maps.incidents_state_map[item_data['state']] if "state" in item_data else "N/A",
            "sys_created_by": item_data['sys_created_by'] if "sys_created_by" in item_data else "N/A",
            "target_link": Core.sdh.build_snow_url(table="incident.do", sys_id=item_data["sys_id"]),
            "sys_updated_on": item_data['sys_updated_on'] if "sys_updated_on" in item_data else "N/A",

        }
        return out_data

    @staticmethod
    def unify_data_for__sc_task(task_data: dict, request_item_data: dict = None) -> dict:
        """
        Unify data for a ServiceNow task.

        :param task_data: Task data
        :param request_item_data: Request item data
        :return: Unified task data
        """
        out_data = {
            "task_effective_number": task_data[
                'task_effective_number'] if "task_effective_number" in task_data else "N/A",
            "short_description": task_data['short_description'] if "short_description" in task_data else "N/A",
            "sys_created_on": task_data['sys_created_on'] if "sys_created_on" in task_data else "N/A",
            "priority": task_data['priority'] if "priority" in task_data else "N/A",
            "sys_updated_by": task_data['sys_updated_by'] if "sys_updated_by" in task_data else "N/A",
            "approval": task_data['approval'] if "approval" in task_data else "N/A",
            "state": snow_maps.sc_task_state_map[task_data['state']] if "state" in task_data else "N/A",
            "target_link": Core.sdh.build_snow_url(table="sc_task.do", sys_id=task_data["sys_id"]),
            "sys_updated_on": task_data['sys_updated_on'] if "sys_updated_on" in task_data else "N/A",

        }
        if request_item_data:
            out_data["sys_created_by"] = request_item_data[
                'sys_created_by'] if "sys_created_by" in request_item_data else "N/A"
        else:
            out_data["sys_created_by"] = "N/A"
        return out_data

    def unify_data_for__change_request(self, _data: dict) -> dict:
        """
        Unify data for a ServiceNow change request.

        :param _data: Change request data
        :return: Unified change request data
        """
        out_data = {
            "task_effective_number": _data[
                'task_effective_number'] if "task_effective_number" in _data else "N/A",
            "short_description": _data['short_description'] if "short_description" in _data else "N/A",
            "sys_created_on": _data['sys_created_on'] if "sys_created_on" in _data else "N/A",
            "priority": _data['priority'] if "priority" in _data else "N/A",
            "sys_updated_by": _data['sys_updated_by'] if "sys_updated_by" in _data else "N/A",
            "approval": _data['approval'] if "approval" in _data else "N/A",
            "state": _data['state'] if "state" in _data else "N/A",
            "sys_created_by": _data['sys_created_by'] if "sys_created_by" in _data else "N/A",
            "target_link": self.build_snow_url(table="change_request.do", sys_id=_data["sys_id"]),
            "sys_updated_on": _data['sys_updated_on'] if "sys_updated_on" in _data else "N/A",

        }
        return out_data