Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var css_1 = require("@emotion/css"); // eslint-disable-line emotion/no-vanilla
var react_2 = require("@emotion/react"); // This is needed to set "speedy" = false (for percy)
var preferences_1 = require("app/actionCreators/preferences");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var global_1 = tslib_1.__importDefault(require("app/styles/global"));
var theme_1 = require("app/utils/theme");
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var Main = /** @class */ (function (_super) {
    tslib_1.__extends(Main, _super);
    function Main() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            theme: _this.themeName === 'dark' ? theme_1.darkTheme : theme_1.lightTheme,
        };
        return _this;
    }
    Main.prototype.componentDidMount = function () {
        preferences_1.loadPreferencesState();
    };
    Main.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (config.theme !== prevProps.config.theme) {
            // eslint-disable-next-line
            this.setState({
                theme: config.theme === 'dark' ? theme_1.darkTheme : theme_1.lightTheme,
            });
        }
    };
    Object.defineProperty(Main.prototype, "themeName", {
        get: function () {
            return configStore_1.default.get('theme');
        },
        enumerable: false,
        configurable: true
    });
    Main.prototype.render = function () {
        return (<react_2.ThemeProvider theme={this.state.theme}>
        <global_1.default isDark={this.props.config.theme === 'dark'} theme={this.state.theme}/>
        <react_2.CacheProvider value={css_1.cache}>{this.props.children}</react_2.CacheProvider>
        {react_dom_1.default.createPortal(<meta name="color-scheme" content={this.themeName}/>, document.head)}
      </react_2.ThemeProvider>);
    };
    return Main;
}(react_1.Component));
exports.default = withConfig_1.default(Main);
//# sourceMappingURL=themeAndStyleProvider.jsx.map