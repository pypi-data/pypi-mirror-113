Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
/**
 * Component to handle demo mode switches
 */
function DemoModeGate(props) {
    var organization = props.organization, children = props.children, _a = props.demoComponent, demoComponent = _a === void 0 ? null : _a;
    if ((organization === null || organization === void 0 ? void 0 : organization.role) === 'member' && configStore_1.default.get('demoMode')) {
        if (typeof demoComponent === 'function') {
            return demoComponent({ children: children });
        }
        return demoComponent;
    }
    return children;
}
exports.default = withOrganization_1.default(DemoModeGate);
//# sourceMappingURL=demoModeGate.jsx.map