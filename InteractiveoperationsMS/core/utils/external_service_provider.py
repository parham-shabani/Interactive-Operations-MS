from rest_framework.exceptions import ValidationError
import requests
import os
from dotenv import load_dotenv
import json
import logging
import urllib.parse

logger = logging.getLogger(__name__)
load_dotenv()

SEND_SINGLE_EMAIL_BY_SENDGRID_URL = os.environ.get('SEND_SINGLE_EMAIL_BY_SENDGRID_URL')
SEND_BULK_EMAIL_BY_SENDGRID_URL = os.environ.get('SEND_BULK_EMAIL_BY_SENDGRID_URL')

SEND_VALIDATION_CODE_BY_KAVENEGAR_URL = os.environ.get('SEND_VALIDATION_CODE_BY_KAVENEGAR_URL')
SIMPLE_SEND_BY_KAVENEGAR_URL = os.environ.get('SIMPLE_SEND_BY_KAVENEGAR_URL')
SEND_ARRAY_BY_KAVENEGAR_URL = os.environ.get('SEND_ARRAY_BY_KAVENEGAR_URL')

"""
****************************************** send email by ServiceProviderMS *******************************************
"""


class UseEmailServiceProviderMSClass:

    @classmethod
    def send_single_email(cls, subject: str, content: str, to_email: str,
                          send_at: str | None = None, ):
        """
        use external_api for send one email to a user using SendGrid.
        """
        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            "subject": subject,
            "content": content,
            "to_email": to_email,
        }
        if send_at:
            params['send_date'] = send_at  # optional

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SEND_SINGLE_EMAIL_BY_SENDGRID_URL + '?' + query_string

        result = requests.post(url, headers=headers)
        logger.info(f"result.status_code:{result.status_code}")

        # status_code = 200  # for test
        if result.status_code == 200:
            result_send_email = result.json()
            # result_send_email = {'data': None, 'message': 'Email sent successfully.', 'status_code': 200,
            #                      'result': True}  # for test
            logger.info(f"result_send_email:{result_send_email}")
            return result_send_email

        else:
            logger.info(f"send_single_email is failed...................")
            raise ValidationError(result.json()['message'])

    @classmethod
    def send_bulk_email(cls, subject: str, content: str, to_emails: list[str],
                        send_at: str | None = None, ):
        """
        use external_api for Send email to a large number of users using SendGrid.
        The total number of recipients must no more than 1000.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            "subject": subject,
            "content": content,
        }
        if send_at:
            params['send_date'] = send_at  # optional

        data = {
            "to_emails": to_emails
        }

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SEND_BULK_EMAIL_BY_SENDGRID_URL + '?' + query_string

        result = requests.post(
            url,
            data=json.dumps(data),  # for get info by request body
            headers=headers)
        logger.info(f"result.status_code:{result.status_code}")

        if result.status_code == 200:
            result_send_email = result.json()
            logger.info(f"result_send_email:{result_send_email}")
            return result_send_email

        else:
            logger.info(f"send_bulk_email is failed...................")
            raise ValidationError(result.json()['message'])

    @classmethod
    def send_bulk_email_by_chunk(cls, subject: str, content: str, to_emails: list[str], num_chunk: int,
                                 send_at: str | None = None, ):
        """
        use external_api for Send email to a large number of users using SendGrid.
        The total number of recipients (to_emails) must no more than 1000.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            "subject": subject,
            "content": content,
        }
        if send_at:
            params['send_date'] = send_at  # optional

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SEND_BULK_EMAIL_BY_SENDGRID_URL + '?' + query_string

        chunks = [to_emails[x:x + num_chunk] for x in range(0, len(to_emails), num_chunk)]

        all_response_202 = []
        all_response_403 = []

        for email_list in chunks:
            data = {"to_emails": email_list}
            result = requests.post(url, data=json.dumps(data), headers=headers)
            logger.info(f"result.status_code:{result.status_code}")

            if result.status_code == 200:
                all_response_202.append(email_list)
                result_send_email = result.json()
                logger.info(f"result_send_email:{result_send_email}")
                # return result_send_email

            else:
                all_response_403.append(email_list)
                logger.info(f"send_bulk_email is failed: {result.json()['message']}")
                # raise ValidationError(result.json()['message'])

        logger.info(f"all_response_202:{all_response_202}")
        logger.info(f"len_all_response_202:{len(all_response_202)}")

        logger.info(f"all_response_403:{all_response_403}")
        logger.info(f"len_all_response_403:{len(all_response_403)}")

        if len(all_response_202) == len(chunks):
            return True
        else:
            return False


"""
****************************************** send sms by ServiceProviderMS ********************************************
"""


class UseSMSServiceProviderMSClass:

    @classmethod
    def send_otp_sms(cls,
                     receptor: str, token: str,
                     token2: str | None = None, token3: str | None = None,
                     send_type: str | None = None, template: str | None = None):
        """
        use external_api for send an otp_sms or otp_call to a user using Kavenegar.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            'receptor': receptor,
            'token': token,
        }
        if token2:
            params['token2'] = token2  # optional
        if token3:
            params['token3'] = token3  # optional
        if send_type:
            params['send_type'] = send_type  # optional, sms vs call
        if template:
            params['template'] = template

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SEND_VALIDATION_CODE_BY_KAVENEGAR_URL + '?' + query_string

        result = requests.post(url, headers=headers)
        logger.info(f"result.status_code:{result.status_code}")

        if result.status_code == 200:
            result_send_sms = result.json()
            # result_send_sms = {}  # for test
            logger.info(f"result_send_sms:{result_send_sms}")
            return result_send_sms

        else:
            logger.info(f"send_otp_sms is failed...................")
            raise ValidationError(result.json()['message'])

    @classmethod
    def send_simple_sms(cls,
                        message: str, receptors: list[str],
                        date: str | None = None,
                        send_type: str | None = None,
                        localid: list[str] | None = None,
                        hide: int | None = None,
                        sender: str | None = None,
                        ):
        """
        use external_api for send sms to a large number of users using Kavenegar.
        The maximum number of simultaneous sending and receiving status per call is 200.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            "message": message,
        }

        if send_type:
            params['send_type'] = send_type  # optional
        if date:
            params['send_date'] = date  # optional
        if hide:
            params['hide'] = hide  # optional
        if sender:
            params['sender'] = sender  # optional

        data = {
            "receptors": receptors,
            "local_id": localid  # optional
        }

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SIMPLE_SEND_BY_KAVENEGAR_URL + '?' + query_string

        result = requests.post(
            url,
            data=json.dumps(data),  # for get info by request body
            headers=headers)
        logger.info(f"result.status_code:{result.status_code}")

        # status_code = 200  # for test
        if result.status_code == 200:
            # if status_code == 200:
            result_send_sms = result.json()
            # result_send_sms = {}  # for test
            logger.info(f"result_send_sms:{result_send_sms}")
            return result_send_sms

        else:
            logger.info(f"send_simple_sms is failed:{result.json()['message']}")
            raise ValidationError(result.json()['message'])

    @classmethod
    def send_simple_sms_by_chunk(cls,
                                 message: str, receptors: list[str], num_chunk: int,
                                 date: str | None = None,
                                 send_type: str | None = None,
                                 localid: list[str] | None = None,
                                 hide: int | None = None,
                                 sender: str | None = None
                                 ):
        """
        use external_api for send sms to a large number of users using Kavenegar.
        The maximum number of simultaneous sending and receiving status per call is 200.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = {
            "message": message,
        }

        if send_type:
            params['send_type'] = send_type  # optional
        if date:
            params['send_date'] = date  # optional
        if hide:
            params['hide'] = hide  # optional
        if sender:
            params['sender'] = sender  # optional
        logger.info(f"params:{params}")

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SIMPLE_SEND_BY_KAVENEGAR_URL + '?' + query_string

        chunks = [receptors[x:x + num_chunk] for x in range(0, len(receptors), num_chunk)]

        all_response_200 = []
        all_response_400 = []

        for mobile_list in chunks:
            data = {
                "receptors": mobile_list,
                "local_id": localid  # optional
            }
            result = requests.post(url, data=json.dumps(data), headers=headers)
            logger.info(f"result.status_code:{result.status_code}")

            if result.status_code == 200:
                all_response_200.append(mobile_list)
                result_send_sms = result.json()
                logger.info(f"result_send_sms:{result_send_sms}")
                # return result_send_sms

            else:
                all_response_400.append(mobile_list)
                logger.info(f"send_simple_sms_by_chunk is failed: {result.json()['message']}")
                # raise ValidationError(result.json()['message'])

        logger.info(f"all_response_200:{all_response_200}")
        logger.info(f"len_all_response_200:{len(all_response_200)}")

        logger.info(f"all_response_400:{all_response_400}")
        logger.info(f"len_all_response_400:{len(all_response_400)}")

        if len(all_response_200) == len(chunks):
            return True
        else:
            return False

    @classmethod
    def send_array_sms(cls,
                       message: list[str], receptors: list[str], sender: list[str],
                       date: str | None = None,
                       send_type: str | None = None,
                       localmessageids: list[str] | None = None,
                       hide: int | None = None
                       ):
        """
        use external_api for send bulk sms using Kavenegar.
        The maximum number of simultaneous sending and receiving status per call is 200.
        """

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

        params = dict()
        if hide:
            params['hide'] = hide  # optional
        if date:
            params['send_date'] = date  # optional

        data = {
            "message": message,
            "receptors": receptors,
            "sender": sender,
            "send_type": send_type,  # optional
            "local_message_ids": localmessageids,  # optional
        }

        # for get info by parameters
        query_string = urllib.parse.urlencode(params)
        url = SEND_ARRAY_BY_KAVENEGAR_URL + '?' + query_string

        result = requests.post(
            url,
            data=json.dumps(data),  # for get info by request body
            headers=headers)
        logger.info(f"result.status_code:{result.status_code}")

        if result.status_code == 200:
            result_send_sms = result.json()
            logger.info(f"result_send_sms:{result_send_sms}")
            return result_send_sms

        else:
            logger.info(f"send_bulk_sms is failed:{result.json()['message']}")
            raise ValidationError(result.json()['message'])
