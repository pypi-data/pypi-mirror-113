Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var locale_1 = require("app/locale");
function ChartFooter(_a) {
    var total = _a.total, yAxisValue = _a.yAxisValue, yAxisOptions = _a.yAxisOptions, onAxisChange = _a.onAxisChange, displayMode = _a.displayMode, displayOptions = _a.displayOptions, onDisplayChange = _a.onDisplayChange;
    var elements = [];
    elements.push(<styles_1.SectionHeading key="total-label">{locale_1.t('Total Events')}</styles_1.SectionHeading>);
    elements.push(total === null ? (<styles_1.SectionValue data-test-id="loading-placeholder" key="total-value">
        &mdash;
      </styles_1.SectionValue>) : (<styles_1.SectionValue key="total-value">{total.toLocaleString()}</styles_1.SectionValue>));
    return (<styles_1.ChartControls>
      <styles_1.InlineContainer>{elements}</styles_1.InlineContainer>
      <styles_1.InlineContainer>
        <optionSelector_1.default title={locale_1.t('Display')} selected={displayMode} options={displayOptions} onChange={onDisplayChange} menuWidth="170px"/>
        <optionSelector_1.default title={locale_1.t('Y-Axis')} selected={yAxisValue} options={yAxisOptions} onChange={onAxisChange}/>
      </styles_1.InlineContainer>
    </styles_1.ChartControls>);
}
exports.default = ChartFooter;
//# sourceMappingURL=chartFooter.jsx.map