Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var mobx_react_1 = require("mobx-react");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var QuickTraceContext = tslib_1.__importStar(require("app/utils/performance/quickTrace/quickTraceContext"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var AnchorLinkManager = tslib_1.__importStar(require("./anchorLinkManager"));
var filter_1 = tslib_1.__importDefault(require("./filter"));
var traceView_1 = tslib_1.__importDefault(require("./traceView"));
var utils_2 = require("./utils");
var waterfallModel_1 = tslib_1.__importDefault(require("./waterfallModel"));
var SpansInterface = /** @class */ (function (_super) {
    tslib_1.__extends(SpansInterface, _super);
    function SpansInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            parsedTrace: utils_2.parseTrace(_this.props.event),
            waterfallModel: new waterfallModel_1.default(_this.props.event),
        };
        _this.handleSpanFilter = function (searchQuery) {
            var waterfallModel = _this.state.waterfallModel;
            waterfallModel.querySpanSearch(searchQuery);
        };
        return _this;
    }
    SpansInterface.getDerivedStateFromProps = function (props, state) {
        if (state.waterfallModel.isEvent(props.event)) {
            return state;
        }
        return tslib_1.__assign(tslib_1.__assign({}, state), { parsedTrace: utils_2.parseTrace(props.event), waterfallModel: new waterfallModel_1.default(props.event) });
    };
    SpansInterface.prototype.renderTraceErrorsAlert = function (_a) {
        var _this = this;
        var isLoading = _a.isLoading, errors = _a.errors, parsedTrace = _a.parsedTrace;
        if (isLoading) {
            return null;
        }
        if (!errors || errors.length <= 0) {
            return null;
        }
        var label = locale_1.tn('There is an error event associated with this transaction event.', "There are %s error events associated with this transaction event.", errors.length);
        // mapping from span ids to the span op and the number of errors in that span
        var errorsMap = {};
        errors.forEach(function (error) {
            if (!errorsMap[error.span]) {
                // first check of the error belongs to the root span
                if (parsedTrace.rootSpanID === error.span) {
                    errorsMap[error.span] = {
                        operation: parsedTrace.op,
                        errorsCount: 0,
                    };
                }
                else {
                    // since it does not belong to the root span, check if it belongs
                    // to one of the other spans in the transaction
                    var span = parsedTrace.spans.find(function (s) { return s.span_id === error.span; });
                    if (!(span === null || span === void 0 ? void 0 : span.op)) {
                        return;
                    }
                    errorsMap[error.span] = {
                        operation: span.op,
                        errorsCount: 0,
                    };
                }
            }
            errorsMap[error.span].errorsCount++;
        });
        return (<AlertContainer>
        <alert_1.default type="error" icon={<icons_1.IconWarning size="md"/>}>
          <ErrorLabel>{label}</ErrorLabel>
          <AnchorLinkManager.Consumer>
            {function (_a) {
                var scrollToHash = _a.scrollToHash;
                return (<list_1.default symbol="bullet">
                {Object.entries(errorsMap).map(function (_a) {
                        var _b = tslib_1.__read(_a, 2), spanId = _b[0], _c = _b[1], operation = _c.operation, errorsCount = _c.errorsCount;
                        return (<listItem_1.default key={spanId}>
                    {locale_1.tct('[errors] in [link]', {
                                errors: locale_1.tn('%s error in ', '%s errors in ', errorsCount),
                                link: (<ErrorLink onClick={utils_2.scrollToSpan(spanId, scrollToHash, _this.props.location)}>
                          {operation}
                        </ErrorLink>),
                            })}
                  </listItem_1.default>);
                    })}
              </list_1.default>);
            }}
          </AnchorLinkManager.Consumer>
        </alert_1.default>
      </AlertContainer>);
    };
    SpansInterface.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, organization = _a.organization;
        var _b = this.state, parsedTrace = _b.parsedTrace, waterfallModel = _b.waterfallModel;
        return (<Container hasErrors={!utils_1.objectIsEmpty(event.errors)}>
        <QuickTraceContext.Consumer>
          {function (quickTrace) {
                var _a;
                return (<AnchorLinkManager.Provider>
              {_this.renderTraceErrorsAlert({
                        isLoading: (quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.isLoading) || false,
                        errors: (_a = quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.currentEvent) === null || _a === void 0 ? void 0 : _a.errors,
                        parsedTrace: parsedTrace,
                    })}
              <mobx_react_1.Observer>
                {function () {
                        return (<Search>
                      <filter_1.default operationNameCounts={waterfallModel.operationNameCounts} operationNameFilter={waterfallModel.operationNameFilters} toggleOperationNameFilter={waterfallModel.toggleOperationNameFilter} toggleAllOperationNameFilters={waterfallModel.toggleAllOperationNameFilters}/>
                      <StyledSearchBar defaultQuery="" query={waterfallModel.searchQuery || ''} placeholder={locale_1.t('Search for spans')} onSearch={_this.handleSpanFilter}/>
                    </Search>);
                    }}
              </mobx_react_1.Observer>
              <panels_1.Panel>
                <mobx_react_1.Observer>
                  {function () {
                        return (<traceView_1.default waterfallModel={waterfallModel} organization={organization}/>);
                    }}
                </mobx_react_1.Observer>
                <GuideAnchorWrapper>
                  <guideAnchor_1.default target="span_tree" position="bottom"/>
                </GuideAnchorWrapper>
              </panels_1.Panel>
            </AnchorLinkManager.Provider>);
            }}
        </QuickTraceContext.Consumer>
      </Container>);
    };
    return SpansInterface;
}(react_1.PureComponent));
var GuideAnchorWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"], ["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"])));
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.hasErrors &&
        "\n  padding: " + space_1.default(2) + " 0;\n\n  @media (min-width: " + p.theme.breakpoints[0] + ") {\n    padding: " + space_1.default(3) + " 0 0 0;\n  }\n  ";
});
var ErrorLink = styled_1.default('a')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var Search = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var AlertContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var ErrorLabel = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
exports.default = ReactRouter.withRouter(withOrganization_1.default(SpansInterface));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map