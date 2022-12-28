FROM visibilityspots/smashing@sha256:0d3a84b70c73c7519225efda03624341fa2585807c78ecdbedbe2c0bf2529944

ADD dashboards/ /dashboards
ADD jobs/ /jobs

RUN echo "" >> /smashing/Gemfile
RUN echo "gem 'mqtt'" >> /smashing/Gemfile ; bundle install

