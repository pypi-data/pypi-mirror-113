Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var isRenderFunc_1 = require("app/utils/isRenderFunc");
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var comingSoon_1 = tslib_1.__importDefault(require("./comingSoon"));
/**
 * Component to handle feature flags.
 */
var Feature = /** @class */ (function (_super) {
    tslib_1.__extends(Feature, _super);
    function Feature() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Feature.prototype.getAllFeatures = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, config = _a.config;
        return {
            configFeatures: config.features ? Array.from(config.features) : [],
            organization: (organization && organization.features) || [],
            project: (project && project.features) || [],
        };
    };
    Feature.prototype.hasFeature = function (feature, features) {
        var shouldMatchOnlyProject = feature.match(/^projects:(.+)/);
        var shouldMatchOnlyOrg = feature.match(/^organizations:(.+)/);
        // Array of feature strings
        var configFeatures = features.configFeatures, organization = features.organization, project = features.project;
        // Check config store first as this overrides features scoped to org or
        // project contexts.
        if (configFeatures.includes(feature)) {
            return true;
        }
        if (shouldMatchOnlyProject) {
            return project.includes(shouldMatchOnlyProject[1]);
        }
        if (shouldMatchOnlyOrg) {
            return organization.includes(shouldMatchOnlyOrg[1]);
        }
        // default, check all feature arrays
        return organization.includes(feature) || project.includes(feature);
    };
    Feature.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, features = _a.features, renderDisabled = _a.renderDisabled, hookName = _a.hookName, organization = _a.organization, project = _a.project, requireAll = _a.requireAll;
        var allFeatures = this.getAllFeatures();
        var method = requireAll ? 'every' : 'some';
        var hasFeature = !features || features[method](function (feat) { return _this.hasFeature(feat, allFeatures); });
        // Default renderDisabled to the ComingSoon component
        var customDisabledRender = renderDisabled === false
            ? false
            : typeof renderDisabled === 'function'
                ? renderDisabled
                : function () { return <comingSoon_1.default />; };
        // Override the renderDisabled function with a hook store function if there
        // is one registered for the feature.
        if (hookName) {
            var hooks = hookStore_1.default.get(hookName);
            if (hooks.length > 0) {
                customDisabledRender = hooks[0];
            }
        }
        var renderProps = {
            organization: organization,
            project: project,
            features: features,
            hasFeature: hasFeature,
        };
        if (!hasFeature && customDisabledRender !== false) {
            return customDisabledRender(tslib_1.__assign({ children: children }, renderProps));
        }
        if (isRenderFunc_1.isRenderFunc(children)) {
            return children(tslib_1.__assign({ renderDisabled: renderDisabled }, renderProps));
        }
        return hasFeature && children ? children : null;
    };
    Feature.defaultProps = {
        renderDisabled: false,
        requireAll: true,
    };
    return Feature;
}(React.Component));
exports.default = withOrganization_1.default(withProject_1.default(withConfig_1.default(Feature)));
//# sourceMappingURL=feature.jsx.map