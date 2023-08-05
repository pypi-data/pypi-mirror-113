Object.defineProperty(exports, "__esModule", { value: true });
exports.isLightweightOrganization = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var withOrganizationMock = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        tslib_1.__extends(WithOrganizationMockWrapper, _super);
        function WithOrganizationMockWrapper() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        WithOrganizationMockWrapper.prototype.render = function () {
            return (<WrappedComponent organization={this.context.organization || TestStubs.Organization()} {...this.props}/>);
        };
        return WithOrganizationMockWrapper;
    }(react_1.Component)),
    _a.contextTypes = {
        organization: sentryTypes_1.default.Organization,
    },
    _a; };
var isLightweightOrganization = function () { };
exports.isLightweightOrganization = isLightweightOrganization;
exports.default = withOrganizationMock;
//# sourceMappingURL=withOrganization.jsx.map