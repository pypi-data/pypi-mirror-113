Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var locale_1 = require("app/locale");
var urls_1 = require("app/utils/discover/urls");
var DiscoverBreadcrumb = /** @class */ (function (_super) {
    tslib_1.__extends(DiscoverBreadcrumb, _super);
    function DiscoverBreadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DiscoverBreadcrumb.prototype.getCrumbs = function () {
        var crumbs = [];
        var _a = this.props, eventView = _a.eventView, event = _a.event, organization = _a.organization, location = _a.location;
        var discoverTarget = organization.features.includes('discover-query')
            ? {
                pathname: urls_1.getDiscoverLandingUrl(organization),
                query: tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, location.query), eventView.generateBlankQueryStringObject()), eventView.getGlobalSelectionQuery()),
            }
            : null;
        crumbs.push({
            to: discoverTarget,
            label: locale_1.t('Discover'),
        });
        if (eventView && eventView.isValid()) {
            crumbs.push({
                to: eventView.getResultsViewUrlTarget(organization.slug),
                label: eventView.name || '',
            });
        }
        if (event) {
            crumbs.push({
                label: locale_1.t('Event Detail'),
            });
        }
        return crumbs;
    };
    DiscoverBreadcrumb.prototype.render = function () {
        return <breadcrumbs_1.default crumbs={this.getCrumbs()}/>;
    };
    DiscoverBreadcrumb.defaultProps = {
        event: undefined,
    };
    return DiscoverBreadcrumb;
}(react_1.Component));
exports.default = DiscoverBreadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map