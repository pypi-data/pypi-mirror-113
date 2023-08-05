Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var locale_1 = require("app/locale");
/**
 * Provide a component that passes a prop to indicate if the current
 * organization doesn't have access to discover results.
 */
function DiscoverFeature(_a) {
    var children = _a.children;
    var noFeatureMessage = locale_1.t('Requires discover feature.');
    var renderDisabled = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>); };
    return (<feature_1.default hookName="feature-disabled:open-discover" features={['organizations:discover-basic']} renderDisabled={renderDisabled}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return children({ hasFeature: hasFeature });
    }}
    </feature_1.default>);
}
exports.default = DiscoverFeature;
//# sourceMappingURL=discoverFeature.jsx.map