from typing import Union

from requests import Response as r_Response
from httpx._models import Response as h_Response


class Reporter:
    def __init__(self, response: Union[r_Response, h_Response]):
        """
        Class for generate response report

        :param response: (requests or) httpx Response
        """
        lines = []
        steps: list[h_Response] = response.history + [response]
        for index, step in enumerate(steps):
            lines.append(''.center(52, "#"))
            lines.append(f' STEP {index + 1} '.center(52, "#"))
            lines.append(''.center(52, "#"))
            lines.append('')
            lines.append(f'R-URL: {step.request.url}')
            lines.append(f'URL: {step.url}')
            lines.append(f'Code: {step.status_code} {step.reason_phrase}')
            lines.append(f'Method: {step.request.method}')
            lines.append('')
            lines.append(' REQUEST '.center(52, "#"))
            lines.append('Headers:')
            lines.append('')
            for k, v in step.request.headers.raw:
                lines.append(f'{k.decode()}: '.ljust(16, " ") + v.decode())
            lines.append('')
            if step.request.method in ['POST', 'PUT', 'DELETE']:
                ...
            lines.append(' RESPONSE '.center(52, "#"))
            lines.append('')
            lines.append('Headers:')
            lines.append('')
            for k, v in step.headers.raw:
                lines.append(f'{k.decode()}: '.ljust(16, " ") + v.decode())
            if step.text:
                lines.append('')
                lines.append(' CONTENT '.center(52, "#"))
                content_lines = step.text.count("\n")
                lines.append(f' END AT {len(lines) + content_lines + 5} LINE '.center(52, "#"))
                lines.append('')
                lines.append(step.text)
                lines.append('')
                lines.append(' END CONTENT '.center(52, "#"))
                lines.append('')
        self.lines = [line + "\n" for line in lines]

    def save(self, name: str) -> str:
        """

        :param name: filename
        :return: report-str
        """
        with open(name, "w+") as rf:
            rf.writelines(self.lines)
        return "".join(self.lines)




