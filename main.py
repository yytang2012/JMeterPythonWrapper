import os
from datetime import datetime

ROOT_DIR = os.path.dirname(__file__)


def now_time():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main(protocol, domain, port, route, feature_type, num_loops, num_threads, jmx_name="test"):
    dir_path = os.path.join(ROOT_DIR, "logs", now_time())
    jmx_template_path = os.path.join(ROOT_DIR, "template.jmx")
    if os.path.exists(dir_path):
        os.removedirs(dir_path)
    os.makedirs(dir_path)
    content = open(jmx_template_path, 'r').read()
    jmx_file = f"{jmx_name}.jmx"
    content = content.replace("customize_num_threads", str(num_threads))
    content = content.replace("customize_num_loops", str(num_loops))
    content = content.replace("customize_domain", domain)
    content = content.replace("customize_protocol", protocol)
    content = content.replace("customize_port", port)
    content = content.replace("customize_route", route)
    content = content.replace("FEATURE_TYPE", feature_type)
    jmx_path = os.path.join(dir_path, jmx_file)
    with open(jmx_path, "w") as f:
        f.write(content)
    exec_app = os.path.join(ROOT_DIR, "apache-jmeter-5.3", "bin", "jmeter")

    out_txt = os.path.join(dir_path, f"{jmx_name}.txt")
    out_result = os.path.join(dir_path, jmx_name)

    cmd = f"{exec_app} -n -t {jmx_path} -l {out_txt} -e -o {out_result}"
    os.system(cmd)


def test_shelf_item_local():
    num_loops = 10
    num_threads = 200
    url = "http://0.0.0.0:9001/v1/predict"
    protocol = "http"
    domain = "0.0.0.0"
    port = "9001"
    route = "/v1/predict"
    feature_type = "SHELF_ITEM_DETECTION"
    main(protocol, domain, port, route, feature_type, num_loops, num_threads)


def test_overseer_azure_stg():
    num_loops = 10
    num_threads = 100
    url = "https://stg-itemrecognition.cld.samsclub.com/v1/overseer"
    protocol = "https"
    domain = "stg-itemrecognition.cld.samsclub.com"
    port = ""
    route = "/v1/overseer"
    feature_type = "SHELF_ITEM_DETECTION"
    main(protocol, domain, port, route, feature_type, num_loops, num_threads)


if __name__ == "__main__":
    test_overseer_azure_stg()
