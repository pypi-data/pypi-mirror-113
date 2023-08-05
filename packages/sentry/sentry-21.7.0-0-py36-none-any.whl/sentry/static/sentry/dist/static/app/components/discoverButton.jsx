Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var discoverFeature_1 = tslib_1.__importDefault(require("app/components/discover/discoverFeature"));
/**
 * Provide a button that turns itself off if the current organization
 * doesn't have access to discover results.
 */
function DiscoverButton(_a) {
    var children = _a.children, buttonProps = tslib_1.__rest(_a, ["children"]);
    return (<discoverFeature_1.default>
      {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<button_1.default disabled={!hasFeature} {...buttonProps}>
          {children}
        </button_1.default>);
        }}
    </discoverFeature_1.default>);
}
exports.default = DiscoverButton;
//# sourceMappingURL=discoverButton.jsx.map