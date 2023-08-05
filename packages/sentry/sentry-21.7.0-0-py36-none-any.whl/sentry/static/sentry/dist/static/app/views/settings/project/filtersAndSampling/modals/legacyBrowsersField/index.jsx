Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var bulkController_1 = tslib_1.__importDefault(require("app/components/bulkController"));
var panels_1 = require("app/components/panels");
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var dynamicSampling_1 = require("app/types/dynamicSampling");
var browser_1 = tslib_1.__importDefault(require("./browser"));
var legacyBrowsers = Object.values(dynamicSampling_1.LegacyBrowser);
function LegacyBrowsersField(_a) {
    var onChange = _a.onChange, _b = _a.selectedLegacyBrowsers, selectedLegacyBrowsers = _b === void 0 ? [] : _b;
    function handleChange(_a) {
        var selectedIds = _a.selectedIds;
        onChange(selectedIds);
    }
    return (<bulkController_1.default pageIds={legacyBrowsers} defaultSelectedIds={selectedLegacyBrowsers} allRowsCount={legacyBrowsers.length} onChange={handleChange} columnsCount={0}>
      {function (_a) {
            var selectedIds = _a.selectedIds, onRowToggle = _a.onRowToggle, onPageRowsToggle = _a.onPageRowsToggle, isPageSelected = _a.isPageSelected;
            return (<StyledPanelTable headers={[
                    '',
                    <switchButton_1.default key="switch" size="lg" isActive={isPageSelected} toggle={function () {
                            onPageRowsToggle(!isPageSelected);
                        }}/>,
                ]}>
          {legacyBrowsers.map(function (legacyBrowser) { return (<browser_1.default key={legacyBrowser} browser={legacyBrowser} isEnabled={selectedIds.includes(legacyBrowser)} onToggle={function () {
                        onRowToggle(legacyBrowser);
                    }}/>); })}
        </StyledPanelTable>);
        }}
    </bulkController_1.default>);
}
exports.default = LegacyBrowsersField;
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"], ["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map