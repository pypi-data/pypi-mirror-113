Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var demoHeader_1 = tslib_1.__importDefault(require("app/components/demo/demoHeader"));
var routes_1 = tslib_1.__importDefault(require("app/routes"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var themeAndStyleProvider_1 = tslib_1.__importDefault(require("./themeAndStyleProvider"));
function Main() {
    return (<themeAndStyleProvider_1.default>
      {configStore_1.default.get('demoMode') && <demoHeader_1.default />}
      <react_router_1.Router history={react_router_1.browserHistory}>{routes_1.default()}</react_router_1.Router>
    </themeAndStyleProvider_1.default>);
}
exports.default = Main;
//# sourceMappingURL=main.jsx.map