Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var rowDetails_1 = require("app/components/performance/waterfall/rowDetails");
var utils_1 = require("app/components/quickTrace/utils");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var urls_1 = require("app/utils/discover/urls");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var constants_1 = require("app/utils/performance/vitals/constants");
var utils_2 = require("app/views/performance/transactionSummary/utils");
var utils_3 = require("app/views/performance/utils");
var styles_1 = require("./styles");
var TransactionDetail = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionDetail, _super);
    function TransactionDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.scrollBarIntoView = function (transactionId) { return function (e) {
            // do not use the default anchor behaviour
            // because it will be hidden behind the minimap
            e.preventDefault();
            var hash = "#txn-" + transactionId;
            _this.props.scrollToHash(hash);
            // TODO(txiao): This is causing a rerender of the whole page,
            // which can be slow.
            //
            // make sure to update the location
            react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, _this.props.location), { hash: hash }));
        }; };
        return _this;
    }
    TransactionDetail.prototype.renderTransactionErrors = function () {
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var errors = transaction.errors;
        if (errors.length === 0) {
            return null;
        }
        return (<alert_1.default system type="error" icon={<icons_1.IconWarning size="md"/>} expand={errors.map(function (error) { return (<rowDetails_1.ErrorMessageContent key={error.event_id}>
            <rowDetails_1.ErrorDot level={error.level}/>
            <rowDetails_1.ErrorLevel>{error.level}</rowDetails_1.ErrorLevel>
            <rowDetails_1.ErrorTitle>
              <link_1.default to={utils_1.generateIssueEventTarget(error, organization)}>
                {error.title}
              </link_1.default>
            </rowDetails_1.ErrorTitle>
          </rowDetails_1.ErrorMessageContent>); })}>
        <rowDetails_1.ErrorMessageTitle>
          {locale_1.tn('An error event occurred in this transaction.', '%s error events occurred in this transaction.', errors.length)}
        </rowDetails_1.ErrorMessageTitle>
      </alert_1.default>);
    };
    TransactionDetail.prototype.renderGoToTransactionButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var eventSlug = urls_1.generateEventSlug({
            id: transaction.event_id,
            project: transaction.project_slug,
        });
        var target = utils_3.getTransactionDetailsUrl(organization, eventSlug, transaction.transaction, omit_1.default(location.query, Object.values(globalSelectionHeader_1.PAGE_URL_PARAM)));
        return (<StyledButton size="xsmall" to={target}>
        {locale_1.t('View Transaction')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderGoToSummaryButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var target = utils_2.transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction.transaction,
            query: omit_1.default(location.query, Object.values(globalSelectionHeader_1.PAGE_URL_PARAM)),
            projectID: String(transaction.project_id),
        });
        return (<StyledButton size="xsmall" to={target}>
        {locale_1.t('View Summary')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderMeasurements = function () {
        var transaction = this.props.transaction;
        var _a = transaction.measurements, measurements = _a === void 0 ? {} : _a;
        var measurementKeys = Object.keys(measurements)
            .filter(function (name) { return Boolean(constants_1.WEB_VITAL_DETAILS["measurements." + name]); })
            .sort();
        if (measurementKeys.length <= 0) {
            return null;
        }
        return (<react_1.Fragment>
        {measurementKeys.map(function (measurement) {
                var _a;
                return (<styles_1.Row key={measurement} title={(_a = constants_1.WEB_VITAL_DETAILS["measurements." + measurement]) === null || _a === void 0 ? void 0 : _a.name}>
            {Number(measurements[measurement].value.toFixed(3)).toLocaleString() + "ms"}
          </styles_1.Row>);
            })}
      </react_1.Fragment>);
    };
    TransactionDetail.prototype.renderTransactionDetail = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var startTimestamp = Math.min(transaction.start_timestamp, transaction.timestamp);
        var endTimestamp = Math.max(transaction.start_timestamp, transaction.timestamp);
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        return (<styles_1.TransactionDetails>
        <table className="table key-value">
          <tbody>
            <styles_1.Row title={<TransactionIdTitle onClick={this.scrollBarIntoView(transaction.event_id)}>
                  Transaction ID
                  <StyledIconAnchor />
                </TransactionIdTitle>} extra={this.renderGoToTransactionButton()}>
              {transaction.event_id}
            </styles_1.Row>
            <styles_1.Row title="Transaction" extra={this.renderGoToSummaryButton()}>
              {transaction.transaction}
            </styles_1.Row>
            <styles_1.Row title="Transaction Status">{transaction['transaction.status']}</styles_1.Row>
            <styles_1.Row title="Span ID">{transaction.span_id}</styles_1.Row>
            <styles_1.Row title="Project">{transaction.project_slug}</styles_1.Row>
            <styles_1.Row title="Start Date">
              {getDynamicText_1.default({
                fixed: 'Mar 19, 2021 11:06:27 AM UTC',
                value: (<react_1.Fragment>
                    <dateTime_1.default date={startTimestamp * 1000}/>
                    {" (" + startTimestamp + ")"}
                  </react_1.Fragment>),
            })}
            </styles_1.Row>
            <styles_1.Row title="End Date">
              {getDynamicText_1.default({
                fixed: 'Mar 19, 2021 11:06:28 AM UTC',
                value: (<react_1.Fragment>
                    <dateTime_1.default date={endTimestamp * 1000}/>
                    {" (" + endTimestamp + ")"}
                  </react_1.Fragment>),
            })}
            </styles_1.Row>
            <styles_1.Row title="Duration">{durationString}</styles_1.Row>
            <styles_1.Row title="Operation">{transaction['transaction.op'] || ''}</styles_1.Row>
            {this.renderMeasurements()}
            <styles_1.Tags location={location} organization={organization} transaction={transaction}/>
          </tbody>
        </table>
      </styles_1.TransactionDetails>);
    };
    TransactionDetail.prototype.render = function () {
        return (<styles_1.TransactionDetailsContainer onClick={function (event) {
                // prevent toggling the transaction detail
                event.stopPropagation();
            }}>
        {this.renderTransactionErrors()}
        {this.renderTransactionDetail()}
      </styles_1.TransactionDetailsContainer>);
    };
    return TransactionDetail;
}(react_1.Component));
var TransactionIdTitle = styled_1.default('a')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var StyledIconAnchor = styled_1.default(icons_1.IconAnchor)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"], ["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(1));
var StyledButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
exports.default = TransactionDetail;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionDetail.jsx.map