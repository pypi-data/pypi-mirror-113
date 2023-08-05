Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var organizationRateLimits_1 = tslib_1.__importDefault(require("./organizationRateLimits"));
var OrganizationRateLimitsContainer = function (props) { return (!props.organization ? null : <organizationRateLimits_1.default {...props}/>); };
exports.default = withOrganization_1.default(OrganizationRateLimitsContainer);
//# sourceMappingURL=index.jsx.map