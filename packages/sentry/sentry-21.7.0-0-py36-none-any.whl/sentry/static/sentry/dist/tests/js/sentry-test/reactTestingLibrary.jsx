Object.defineProperty(exports, "__esModule", { value: true });
exports.mountWithTheme = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var css_1 = require("@emotion/css");
var react_2 = require("@emotion/react");
var react_3 = require("@testing-library/react");
var theme_1 = require("app/utils/theme");
function createProvider(contextDefs) {
    var _a;
    return _a = /** @class */ (function (_super) {
            tslib_1.__extends(ContextProvider, _super);
            function ContextProvider() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            ContextProvider.prototype.getChildContext = function () {
                return contextDefs.context;
            };
            ContextProvider.prototype.render = function () {
                return this.props.children;
            };
            return ContextProvider;
        }(react_1.Component)),
        _a.childContextTypes = contextDefs.childContextTypes,
        _a;
}
function makeAllTheProviders(context) {
    return function (_a) {
        var children = _a.children;
        var ContextProvider = context ? createProvider(context) : react_1.Fragment;
        return (<ContextProvider>
        <react_2.CacheProvider value={css_1.cache}>
          <react_2.ThemeProvider theme={theme_1.lightTheme}>{children}</react_2.ThemeProvider>
        </react_2.CacheProvider>
      </ContextProvider>);
    };
}
/**
 * Migrating from enzyme? Pass context via the options object
 * Before
 * mountWithTheme(<Something />, routerContext);
 * After
 * mountWithTheme(<Something />, {context: routerContext});
 */
var mountWithTheme = function (ui, options) {
    var _a = options !== null && options !== void 0 ? options : {}, context = _a.context, otherOptions = tslib_1.__rest(_a, ["context"]);
    var AllTheProviders = makeAllTheProviders(context);
    return react_3.render(ui, tslib_1.__assign({ wrapper: AllTheProviders }, otherOptions));
};
exports.mountWithTheme = mountWithTheme;
tslib_1.__exportStar(require("@testing-library/react"), exports);
//# sourceMappingURL=reactTestingLibrary.jsx.map