Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var badgeDisplayName_1 = tslib_1.__importDefault(require("app/components/idBadge/badgeDisplayName"));
var baseBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/baseBadge"));
var OrganizationBadge = function (_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, organization = _a.organization, props = tslib_1.__rest(_a, ["hideOverflow", "organization"]);
    return (<baseBadge_1.default displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{organization.slug}</badgeDisplayName_1.default>} organization={organization} {...props}/>);
};
exports.default = OrganizationBadge;
//# sourceMappingURL=organizationBadge.jsx.map