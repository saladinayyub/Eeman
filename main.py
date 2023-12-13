import sys
import gi
import setup

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa E:402

app_name = "Eeman"


class WelcomeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 500)
        self.set_title(f"As-salamu alaykum - {app_name}")

        self.box_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL, vexpand=True
        )
        self.set_child(self.box_main)

        # Carousel
        self.carousel = Adw.Carousel(
            hexpand=True, vexpand=True, allow_scroll_wheel=True, allow_long_swipes=False
        )
        self.box_main.append(self.carousel)

        # Indicator
        self.stk_indicator = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.CROSSFADE
        )
        self.box_main.append(self.stk_indicator)
        self.carousel_dots = Adw.CarouselIndicatorDots(carousel=self.carousel)
        self.stk_indicator.add_titled(self.carousel_dots, "page0", "page0")
        # Page 1 - Welcome Page
        self.page1 = Adw.StatusPage(
            title="As-salamu alaykum !",
            description="we will run through the setup process now...",
            icon_name="preferences-desktop-screensaver-symbolic",
            hexpand=True,
            vexpand=True,
        )
        self.carousel.append(self.page1)
        # Page 2 - Setup Page
        self.page2 = Gtk.Box(
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        self.prfbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_start=20,
            margin_end=20,
        )
        self.carousel.append(self.page2)
        self.clamp = Adw.Clamp()
        self.page2.append(self.clamp)
        self.listbox1 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox1.get_style_context().add_class("boxed-list")
        self.listbox2 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox2.get_style_context().add_class("boxed-list")
        self.prfgr_setup = Adw.PreferencesGroup(title="Setup")
        self.prfgr_appearance = Adw.PreferencesGroup(title="Appearance")
        self.prfgr_appearance.add(self.listbox2)
        self.prfgr_setup.add(self.listbox1)
        self.clamp.set_child(self.prfbox)
        self.prfbox.append(self.prfgr_setup)
        self.prfbox.append(self.prfgr_appearance)
        self.prfgr_appearance.set_margin_top(10)

        self.location_setting = Adw.ComboRow(title="Location Mode")
        self.location_mode = Gtk.StringList()
        self.location_mode.append("Automatic using IP")
        self.location_mode.append("Manual (City, Country)")
        self.location_setting.set_model(self.location_mode)
        self.location_setting.connect(
            "notify::selected-item", self.on_location_mode_set
        )
        self.listbox1.append(self.location_setting)

        self.method_setting = Adw.ComboRow(title="Calculation Method")
        self.method_mode = Gtk.StringList()
        self.method_mode.append("Automatic (Nearest)")
        self.method_mode.append("Manual (Choose Method)")
        self.method_setting.set_model(self.method_mode)
        self.listbox1.append(self.method_setting)

        self.dark_theme_setting = Adw.ActionRow(title="Dark theme")
        self.dark_theme_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.dark_theme_setting.add_suffix(self.dark_theme_switch)
        self.dark_theme_switch.connect("state-set", self.set_theme)
        self.listbox2.append(self.dark_theme_setting)

    def on_location_mode_set(self, location_setting, event):
        if "Automatic" in self.location_setting.get_selected_item().get_string():
            setup.get_location_auto()
            print(setup.city)
            print(setup.country)
        if "Manual" in self.location_setting.get_selected_item().get_string():
            print("ask for manual location")

    def set_theme(self, dark_theme_switch, state):
        app = self.get_application()
        sm = app.get_style_manager()
        if state:
            sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        else:
            sm.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = WelcomeWindow(application=app)
        self.win.present()


app = MyApp(application_id="sh.shuriken.Eeman")
app.run(sys.argv)
