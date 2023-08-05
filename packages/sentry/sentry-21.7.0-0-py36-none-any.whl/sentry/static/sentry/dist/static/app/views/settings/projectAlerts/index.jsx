Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var ProjectAlerts = function (_a) {
    var children = _a.children, organization = _a.organization;
    return (<access_1.default organization={organization} access={['project:write']}>
    {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<feature_1.default organization={organization} features={['incidents']}>
        {function (_a) {
                    var hasMetricAlerts = _a.hasFeature;
                    return (<React.Fragment>
            {React.isValidElement(children) &&
                            React.cloneElement(children, {
                                organization: organization,
                                canEditRule: hasAccess,
                                hasMetricAlerts: hasMetricAlerts,
                            })}
          </React.Fragment>);
                }}
      </feature_1.default>);
        }}
  </access_1.default>);
};
exports.default = ProjectAlerts;
//# sourceMappingURL=index.jsx.map