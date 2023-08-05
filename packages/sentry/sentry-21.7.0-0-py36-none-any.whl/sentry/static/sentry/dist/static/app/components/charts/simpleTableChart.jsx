Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panelTable_1 = tslib_1.__importStar(require("app/components/panels/panelTable"));
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var utils_1 = require("app/views/eventsV2/utils");
var SimpleTableChart = /** @class */ (function (_super) {
    tslib_1.__extends(SimpleTableChart, _super);
    function SimpleTableChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SimpleTableChart.prototype.renderRow = function (index, row, tableMeta, columns) {
        var _a = this.props, location = _a.location, organization = _a.organization;
        return columns.map(function (column) {
            var fieldRenderer = fieldRenderers_1.getFieldRenderer(column.name, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            return <div key={index + ":" + column.name}>{rendered}</div>;
        });
    };
    SimpleTableChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, loading = _a.loading, fields = _a.fields, metadata = _a.metadata, data = _a.data, title = _a.title;
        var meta = metadata !== null && metadata !== void 0 ? metadata : {};
        var columns = utils_1.decodeColumnOrder(fields.map(function (field) { return ({ field: field }); }));
        return (<react_1.Fragment>
        {title && <h4>{title}</h4>}
        <StyledPanelTable className={className} isLoading={loading} headers={columns.map(function (column, index) {
                var align = fields_1.fieldAlignment(column.name, column.type, meta);
                return (<HeadCell key={index} align={align}>
                {column.name}
              </HeadCell>);
            })}>
          {data === null || data === void 0 ? void 0 : data.map(function (row, index) { return _this.renderRow(index, row, meta, columns); })}
        </StyledPanelTable>
      </react_1.Fragment>);
    };
    return SimpleTableChart;
}(react_1.Component));
var StyledPanelTable = styled_1.default(panelTable_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-radius: 0;\n  border-left: 0;\n  border-right: 0;\n  border-bottom: 0;\n\n  margin: 0;\n  ", " {\n    height: min-content;\n  }\n"], ["\n  border-radius: 0;\n  border-left: 0;\n  border-right: 0;\n  border-bottom: 0;\n\n  margin: 0;\n  " /* sc-selector */, " {\n    height: min-content;\n  }\n"])), /* sc-selector */ panelTable_1.PanelTableHeader);
var HeadCell = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
exports.default = withOrganization_1.default(SimpleTableChart);
var templateObject_1, templateObject_2;
//# sourceMappingURL=simpleTableChart.jsx.map