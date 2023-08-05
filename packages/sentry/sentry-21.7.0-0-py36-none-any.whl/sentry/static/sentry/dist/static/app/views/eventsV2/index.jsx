Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var DiscoverContainer = /** @class */ (function (_super) {
    tslib_1.__extends(DiscoverContainer, _super);
    function DiscoverContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DiscoverContainer.prototype.renderNoAccess = function () {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    };
    DiscoverContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<feature_1.default features={['discover-basic']} organization={organization} hookName="feature-disabled:discover2-page" renderDisabled={this.renderNoAccess}>
        {children}
      </feature_1.default>);
    };
    return DiscoverContainer;
}(react_1.Component));
exports.default = withOrganization_1.default(DiscoverContainer);
//# sourceMappingURL=index.jsx.map