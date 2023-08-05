Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var utils_1 = require("app/views/eventsV2/utils");
var columnEditCollection_1 = tslib_1.__importDefault(require("./columnEditCollection"));
var ColumnEditModal = /** @class */ (function (_super) {
    tslib_1.__extends(ColumnEditModal, _super);
    function ColumnEditModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            columns: _this.props.columns,
        };
        _this.handleChange = function (columns) {
            _this.setState({ columns: columns });
        };
        _this.handleApply = function () {
            _this.props.onApply(_this.state.columns);
            _this.props.closeModal();
        };
        return _this;
    }
    ColumnEditModal.prototype.componentDidMount = function () {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'discover_v2.column_editor.open',
            eventName: 'Discoverv2: Open column editor',
            organization_id: parseInt(organization.id, 10),
        });
    };
    ColumnEditModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, tagKeys = _a.tagKeys, measurementKeys = _a.measurementKeys, spanOperationBreakdownKeys = _a.spanOperationBreakdownKeys, organization = _a.organization;
        var fieldOptions = utils_1.generateFieldOptions({
            organization: organization,
            tagKeys: tagKeys,
            measurementKeys: measurementKeys,
            spanOperationBreakdownKeys: spanOperationBreakdownKeys,
        });
        return (<react_1.Fragment>
        <Header closeButton>
          <h4>{locale_1.t('Edit Columns')}</h4>
        </Header>
        <Body>
          <Instruction>
            {locale_1.tct('To group events, add [functionLink: functions] f(x) that may take in additional parameters. [tagFieldLink: Tag and field] columns will help you view more details about the events (i.e. title).', {
                functionLink: (<externalLink_1.default href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns"/>),
                tagFieldLink: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/search/#event-properties"/>),
            })}
          </Instruction>
          <columnEditCollection_1.default columns={this.state.columns} fieldOptions={fieldOptions} onChange={this.handleChange} organization={organization}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default priority="default" href={constants_1.DISCOVER2_DOCS_URL} external>
              {locale_1.t('Read the Docs')}
            </button_1.default>
            <button_1.default label={locale_1.t('Apply')} priority="primary" onClick={this.handleApply}>
              {locale_1.t('Apply')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    return ColumnEditModal;
}(react_1.Component));
var Instruction = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
var modalCss = react_2.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: auto;\n    max-width: 900px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    width: auto;\n    max-width: 900px;\n  }\n"])), theme_1.default.breakpoints[1]);
exports.modalCss = modalCss;
exports.default = ColumnEditModal;
var templateObject_1, templateObject_2;
//# sourceMappingURL=columnEditModal.jsx.map