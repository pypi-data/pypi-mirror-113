Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var panels_1 = require("app/components/panels");
var EmptyState = function (_a) {
    var children = _a.children;
    return (<panels_1.Panel>
    <panels_1.PanelBody>
      <emptyStateWarning_1.default>
        <p>{children}</p>
      </emptyStateWarning_1.default>
    </panels_1.PanelBody>
  </panels_1.Panel>);
};
exports.default = EmptyState;
//# sourceMappingURL=emptyState.jsx.map