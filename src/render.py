import logging
import jinja2

log = logging.getLogger()
log.setLevel(logging.WARN)


def render(measurements, coordinates):
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates/")
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = templateEnv.get_template("default.html")

    markers = []
    for m in measurements:
        name = m['location']
        value = m['measurement']
        latitude, longitude = coordinates[name]

        markers.append(f'{latitude},{longitude},{name},{value}')

    page = template.render(markers=markers)
    log.info(page)

    return page