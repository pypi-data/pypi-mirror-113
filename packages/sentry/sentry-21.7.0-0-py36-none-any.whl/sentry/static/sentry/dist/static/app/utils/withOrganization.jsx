Object.defineProperty(exports, "__esModule", { value: true });
exports.isLightweightOrganization = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var withOrganization = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        tslib_1.__extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _a = this.props, organization = _a.organization, props = tslib_1.__rest(_a, ["organization"]);
            return (<WrappedComponent {...tslib_1.__assign({ organization: organization !== null && organization !== void 0 ? organization : this.context.organization }, props)}/>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withOrganization(" + getDisplayName_1.default(WrappedComponent) + ")",
    _a.contextTypes = {
        organization: sentryTypes_1.default.Organization,
    },
    _a; };
function isLightweightOrganization(organization) {
    var castedOrg = organization;
    return !(castedOrg.projects && castedOrg.teams);
}
exports.isLightweightOrganization = isLightweightOrganization;
exports.default = withOrganization;
//# sourceMappingURL=withOrganization.jsx.map