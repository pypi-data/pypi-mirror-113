import json
import os
import sys
from itertools import chain
from pydoc import html

import mistletoe
import requests
from mistletoe import BaseRenderer, block_token
from requests.auth import HTTPBasicAuth

config = {}
config_uri = os.path.expanduser('~') + '/.jira_tool.json'


class JIRARenderer(BaseRenderer):
    """
    JIRA renderer class.

    See mistletoe.base_renderer module for more info.
    """

    def __init__(self, *extras):
        """
        Args:
            extras (list): allows subclasses to add even more custom tokens.
        """
        self.listTokens = []
        super().__init__(*chain([block_token.HTMLBlock, mistletoe.span_token.HTMLSpan], extras))

    def render_strong(self, token):
        template = '*{}*'
        return template.format(self.render_inner(token))

    def render_emphasis(self, token):
        template = '_{}_'
        return template.format(self.render_inner(token))

    def render_inline_code(self, token):
        template = '{{{{{}}}}}'
        return template.format(self.render_inner(token))

    def render_strikethrough(self, token):
        template = '-{}-'
        return template.format(self.render_inner(token))

    def render_image(self, token):
        template = '!{src}!'
        inner = self.render_inner(token)
        return template.format(src=token.src)

    def render_link(self, token):
        template = '[{inner}|{target}]'
        target = escape_url(token.target)
        inner = self.render_inner(token)
        return template.format(target=target, inner=inner)

    def render_auto_link(self, token):
        template = '[{target}]'
        target = escape_url(token.target)
        # inner = self.render_inner(token)
        return template.format(target=target)

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    @staticmethod
    def render_raw_text(token):
        return html.escape(token.content)

    @staticmethod
    def render_html_span(token):
        return token.content

    def render_heading(self, token):
        template = 'h{level}. {inner}\n'
        inner = self.render_inner(token)
        return template.format(level=token.level, inner=inner)

    def render_quote(self, token):
        template = 'bq. {inner}\n'
        return template.format(inner=self.render_inner(token))

    def render_paragraph(self, token):
        return '{}\n'.format(self.render_inner(token))

    def render_block_code(self, token):
        # template = '<pre>\n<code{attr}>\n{inner}</code>\n</pre>\n'
        # if token.language:
        #     attr = ' class="{}"'.format('lang-{}'.format(token.language))
        # else:
        #     attr = ''

        template = '{{code:{attr}}}\n{inner}{{code}}\n'
        if token.language:
            attr = '{}'.format(token.language)
        else:
            attr = ''

        inner = self.render_inner(token)
        return template.format(attr=attr, inner=inner)

    def render_list(self, token):
        inner = self.render_inner(token)
        return inner

    def render_list_item(self, token):
        template = '{prefix} {inner}\n'
        prefix = ''.join(self.listTokens)
        result = template.format(prefix=prefix, inner=self.render_inner(token))
        return result

    def render_inner(self, token):
        if isinstance(token, block_token.List):
            if token.start:
                self.listTokens.append('#')
            else:
                self.listTokens.append('*')

        rendered = [self.render(child) for child in token.children]

        if isinstance(token, block_token.List):
            del (self.listTokens[-1])

        return ''.join(rendered)

    def render_table(self, token):
        # This is actually gross and I wonder if there's a better way to do it.
        #
        # The primary difficulty seems to be passing down alignment options to
        # reach individual cells.
        template = '{inner}\n'
        if hasattr(token, 'header'):
            head_template = '{inner}'
            header = token.children[0]
            head_inner = self.render_table_row(header, True)
            head_rendered = head_template.format(inner=head_inner)

        else:
            head_rendered = ''

        body_template = '{inner}'
        body_inner = self.render_inner(token)
        body_rendered = body_template.format(inner=body_inner)
        return template.format(inner=head_rendered + body_rendered)

    def render_table_row(self, token, is_header=False):
        if is_header:
            template = '{inner}||\n'
        else:
            template = '{inner}|\n'

        inner = ''.join([self.render_table_cell(child, is_header)
                         for child in token.children])

        return template.format(inner=inner)

    def render_table_cell(self, token, in_header=False):
        if in_header:
            template = '||{inner}'
        else:
            template = '|{inner}'

        inner = self.render_inner(token)
        return template.format(inner=inner)

    @staticmethod
    def render_thematic_break(token):
        return '----\n'

    @staticmethod
    def render_line_break(token):
        return '\\\\\n'

    @staticmethod
    def render_html_block(token):
        return token.content

    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        return self.render_inner(token)


def escape_url(raw):
    """
    Escape urls to prevent code injection craziness. (Hopefully.)
    """
    from urllib.parse import quote
    return quote(raw, safe='/#:')


def read_config():
    config_file = open(config_uri, 'r')
    config_json = config_file.read()
    global config
    config = json.loads(config_json)
    config['file_base_uri'] = config['file_base_uri'].replace("~", os.path.expanduser('~'))
    return config


def upload_attr(card_number, image_urls):
    url = "https://itsc-jira.daimler.com/jira/rest/api/2/issue/" + card_number + "/attachments"

    payload = {}

    files = []
    for image_url in image_urls:
        uri_array = image_url.split("/")
        img_file_name = uri_array[len(uri_array) - 1]
        files.append(('file', (img_file_name,
                               open(image_url, 'rb'), 'image/png')))
    headers = {
        'X-Atlassian-Token': 'no-check',
        'Authorization': 'Basic c2hpd2VpLmZ1LWV4dDpwYXNzd29yZEAxMjM0',
        'Cookie': 'JSESSIONID=577BB4DF3437151A22A98FEF29FE3246; atlassian.xsrf.token=BMI4-1R31-1BHC-T760_af131527a8dc4702f9074d59bd45bbcf19b15fc5_lin; BIGipServeritsc-jira_117.121.110.148_pool=!Vbl3pi5IV6gzJlSGVXRtvx59bU/E2JSq7J5JSl47Kmxvz9Q5OgT54/v+LRezXsThrgcTSThrqcuLU8A='
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text)


def replace_image_to_jira_attr(card_number, url, file, desc):
    fo = open(url + '/' + file, "r")
    mark_down_content = fo.read()
    content_array = mark_down_content.split("![image")
    image_urls = []
    for i in range(len(content_array)):
        if i != 0:
            content_burst = content_array[i]
            content_lines = content_burst.split("\n")
            img_line = content_lines[0]
            img_line_array = img_line.split("](")
            img_url = img_line_array[1]
            img_url = img_url.replace(")", "")
            # upload_attr(card_number, img_url)
            print(img_url)
            image_urls.append(img_url)
    if len(image_urls) > 0:
        attr_infos = upload_attr(card_number=card_number, image_urls=image_urls)
        for img_url in image_urls:
            uri_array = img_url.split("/")
            img_file_name = uri_array[len(uri_array) - 1]
            desc = desc.replace(img_url, img_file_name + '|thumbnail')
        print(attr_infos)
    print(desc)
    return desc


def ignored_mermaid(desc):
    formatted_desc = ''
    desc_bursts = desc.split('{code:mermaid}')
    for i in range(len(desc_bursts)):
        if i == 0:
            formatted_desc = formatted_desc + desc_bursts[0]
        else:
            desc_burst = desc_bursts[i]
            desc_burst_twice = desc_burst.split("{code}")
            for j in range(len(desc_burst_twice)):
                if j != 0 and j != 1:
                    formatted_desc = formatted_desc + "{code}" + desc_burst_twice[j]
                if j == 1:
                    formatted_desc = formatted_desc + desc_burst_twice[j]
    print(formatted_desc)
    return formatted_desc


def edit_jira_card(card_number, desc):
    url = config['host'] + "/jira/rest/api/2/issue/" + card_number
    payload = json.dumps({
        "fields": {
            "description": desc
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, auth=HTTPBasicAuth(config['name'], config['password']), headers=headers,
                                data=payload)
    print(response)


def get_markdown_info_with_jira_format(url, file, card_no):
    fo = open(url + '/' + file, "r")
    rendered = mistletoe.markdown(fo, JIRARenderer)
    rendered = replace_image_to_jira_attr(card_no, url, file, rendered)
    rendered = ignored_mermaid(rendered)
    return rendered


def main(args=None):
    read_config()

    if len(sys.argv) == 3:
        file_url = config['file_base_uri'] + sys.argv[1]
        card_no = sys.argv[2]
        file_name = card_no + ".md"
        print(card_no)
        jira_desc = get_markdown_info_with_jira_format(file_url, file_name, card_no)
        print(jira_desc)
        edit_jira_card(card_no, jira_desc)
        return 0
    else:
        file_url = config['file_base_uri'] + sys.argv[1]
        files = os.listdir(file_url)  # 得到文件夹下的所有文件名称
        for file_name in files:  # 遍历文件夹
            if not os.path.isdir(file_name):
                card_no = file_name.replace(".md", "")
                print(card_no)
                jira_desc = get_markdown_info_with_jira_format(file_url, file_name, card_no)
                print(jira_desc)
                edit_jira_card(card_no, jira_desc)
        return 0


if __name__ == "__main__":
    sys.exit(main())
