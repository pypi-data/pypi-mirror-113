Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var locale_1 = require("app/locale");
var queryString_1 = require("app/utils/queryString");
var utils_1 = require("./transactionSummary/transactionVitals/utils");
var utils_2 = require("./transactionSummary/utils");
var utils_3 = require("./vitalDetail/utils");
var utils_4 = require("./utils");
var Breadcrumb = /** @class */ (function (_super) {
    tslib_1.__extends(Breadcrumb, _super);
    function Breadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Breadcrumb.prototype.getCrumbs = function () {
        var crumbs = [];
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, vitalName = _a.vitalName, eventSlug = _a.eventSlug, traceSlug = _a.traceSlug, transactionComparison = _a.transactionComparison, realUserMonitoring = _a.realUserMonitoring;
        var performanceTarget = {
            pathname: utils_4.getPerformanceLandingUrl(organization),
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { 
                // clear out the transaction name
                transaction: undefined }),
        };
        crumbs.push({
            to: performanceTarget,
            label: locale_1.t('Performance'),
            preserveGlobalSelection: true,
        });
        if (vitalName) {
            var rumTarget = utils_3.vitalDetailRouteWithQuery({
                orgSlug: organization.slug,
                vitalName: 'fcp',
                projectID: queryString_1.decodeScalar(location.query.project),
                query: location.query,
            });
            crumbs.push({
                to: rumTarget,
                label: locale_1.t('Vital Detail'),
                preserveGlobalSelection: true,
            });
        }
        else if (transactionName) {
            if (realUserMonitoring) {
                var rumTarget = utils_1.vitalsRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: queryString_1.decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: rumTarget,
                    label: locale_1.t('Web Vitals'),
                    preserveGlobalSelection: true,
                });
            }
            else {
                var summaryTarget = utils_2.transactionSummaryRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: queryString_1.decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: summaryTarget,
                    label: locale_1.t('Transaction Summary'),
                    preserveGlobalSelection: true,
                });
            }
        }
        if (transactionName && eventSlug) {
            crumbs.push({
                to: '',
                label: locale_1.t('Event Details'),
            });
        }
        else if (transactionComparison) {
            crumbs.push({
                to: '',
                label: locale_1.t('Compare to Baseline'),
            });
        }
        else if (traceSlug) {
            crumbs.push({
                to: '',
                label: locale_1.t('Trace View'),
            });
        }
        return crumbs;
    };
    Breadcrumb.prototype.render = function () {
        return <breadcrumbs_1.default crumbs={this.getCrumbs()}/>;
    };
    return Breadcrumb;
}(react_1.Component));
exports.default = Breadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map