Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var item_1 = tslib_1.__importDefault(require("./item"));
var ContextSummaryNoSummary = function (_a) {
    var title = _a.title;
    return (<item_1.default icon={<span className="context-item-icon"/>}>
    <h3 data-test-id="no-summary-title">{title}</h3>
  </item_1.default>);
};
exports.default = ContextSummaryNoSummary;
//# sourceMappingURL=contextSummaryNoSummary.jsx.map