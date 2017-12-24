from string import Template
import yaml

def get_coordinators():
    coord_template = Template('''
        <div class="col-lg-3 col-md-6 col-12 mt-3 mb-3 d-flex">
          <div class="card card-dark" style="flex: 1;">
            <img class="card-img-top" src="https://avatars.githubusercontent.com/$github" alt="$name">
            <div class="card-body">
              <h4 class="card-title"> $name </h4>
              <h6 class="card-subtitle text-muted"> $position </h6>
            </div>
          </div>
        </div>
    ''')

    with open("coordinators.yml", "r") as coord_yml:
        coords = yaml.load(coord_yml)

    render  = ''' <h1 style="text-align: center;"> Coordinators </h1> <br>'''
    render += ''' <div class="row mb-5"> '''

    for coord in coords:
        render += coord_template.substitute({
            "name": coord["name"],
            "github": coord["github"],
            "position": coord["position"]
        })

    render += ''' </div> '''
