from traitlets.config.manager import BaseJSONConfigManager

########################################################################################################################
## build_footer()
########################################################################################################################
from string import Template

def build_footer():
    footer = Template('''
        <footer id="slide_foot">
          <div  id="slide_foot-brand">
            <span class="ucfsigai-brand"></span>
          </div>
          <div  id="slide_foot-unit">
            <span class="text-gold"> U$lec_unit_num: </span>&nbsp;<span class="text-white"> $lec_unit_nam </span>
          </div>
          <a    id="slide_foot_attend" href="$attend_url">
              <span class="text-white"> $attend_url </span>
          </a>
          <div  id="slide_foot_date">
            <span class="text-white"> $date </span>
          </div>
        </footer>
    ''')

    path = "/root/.jupyter/nbconfig"
    cm = BaseJSONConfigManager(config_dir=path)
    cm.update("livereveal", {
        "autolaunch": true,
        "footer": footer.substitute(),
    })
