Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var AlertsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(AlertsContainer, _super);
    function AlertsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertsContainer.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization;
        return (<feature_1.default organization={organization} features={['incidents']}>
        {function (_a) {
                var hasMetricAlerts = _a.hasFeature;
                return (<react_1.Fragment>
            {children && react_1.isValidElement(children)
                        ? react_1.cloneElement(children, {
                            organization: organization,
                            hasMetricAlerts: hasMetricAlerts,
                        })
                        : children}
          </react_1.Fragment>);
            }}
      </feature_1.default>);
    };
    return AlertsContainer;
}(react_1.Component));
exports.default = withOrganization_1.default(AlertsContainer);
//# sourceMappingURL=index.jsx.map