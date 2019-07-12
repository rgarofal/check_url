import logging.config
import concurrent.futures
import urllib.request
import urllib.error


URLS = ['https://webapp-test.fastweb.it/tmm/login.xhtml']


MAX_TEMPTS = 100000
FILE_NAME_LOG ='E:\Document_rgarofal\WorkingEnv\TMM_WORKING\log_checks\check_TMM.log'

def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


def open_url(url, timeout):

        with urllib.request.urlopen(url, timeout=timeout) as conn:
            data = conn.read()
            return data


if __name__ == '__main__':

  logging.basicConfig(filename=FILE_NAME_LOG, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filemode='a')
  with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
   
    future_to_url = {executor.submit(load_url, URLS[0], 60): id for count in range(1, MAX_TEMPTS)}

    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            print('Success')
        except urllib.error.HTTPError as e:
            print('Errore open_url')
            if e.code != 200:
                print(e.code)
                logging.info( 'Code = %d' %e.code )
                print(e.reason)
                logging.info( 'Reason = %s' % e.reason)
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))

    logging.shutdown()