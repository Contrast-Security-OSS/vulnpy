ARG PYTHON_VERSION=3.8
# FROM python:${PYTHON_VERSION}-slim
FROM python:${PYTHON_VERSION}-bullseye
# ARG PYPI_MIRROR="https://pypi.org/simple"
ARG PYPI_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"
ARG DEBIAN_MIRROR="mirrors.aliyun.com"
RUN if test "x${DEBIAN_MIRROR}" != "x"; then sed -i "s@deb.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list; fi \
  && if test "x${DEBIAN_MIRROR}" != "x"; then sed -i "s@security.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list; fi \
  && apt-get update && apt-get install -y build-essential autoconf gcc make cmake
RUN git clone https://github.com/HXSecurity/DongTai-agent-python.git /DongTai-agent-python
COPY config.example.json config.json* /DongTai-agent-python/dongtai_agent_python/

WORKDIR /vulnpy

COPY . .

RUN pip install -e ".[flask]"  -i ${PYPI_MIRROR} \
  && pip install /DongTai-agent-python/
ENV PORT="3010"
ENV FRAMEWORK="flask"
ENV HOST="0.0.0.0"
ENV VULNPY_USE_CONTRAST="true"

CMD make ${FRAMEWORK}
