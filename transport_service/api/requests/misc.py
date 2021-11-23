import os
import requests
from flask import Blueprint, make_response
from transport_service.logging import mainLogger

def _checkValhalla():
    url = os.environ['VALHALLA_URL']
    r = requests.get(url + '/status')
    mainLogger.debug("_checkValhalla(): Connected to %s", url)
    if len(r.json().keys()) > 0:
        raise Exception(r.json())

bp = Blueprint('misc', __name__)

@bp.route("/health", methods=['GET'])
def health():
    """**Flask GET rule**

    Perform basic health checks.
    ---
    get:
        summary: Get health status.
        tags:
            - Misc
        responses:
            200:
                description: An object with status information.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status:
                                    type: string
                                    enum:
                                        - OK
                                        - FAILED
                                    description: A status of 'OK' or 'FAILED'.
                                details:
                                    type: object
                                    description: The reason of failure for each component, or 'OK' if not failed.
                                    properties:
                                        valhalla:
                                            type: string
                                            example: OK
    """
    mainLogger.info('Performing health checks...')
    msg = {'valhalla': 'OK'}
    status = True

    try:
        _checkValhalla()
    except Exception as e:
        msg['valhalla'] = str(e)
        status = False

    return make_response({'status': 'OK' if status else 'FAILED', 'details': msg}, 200)
