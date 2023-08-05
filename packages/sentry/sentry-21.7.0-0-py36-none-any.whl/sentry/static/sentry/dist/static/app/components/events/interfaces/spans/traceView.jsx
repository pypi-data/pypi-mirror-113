Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var mobx_react_1 = require("mobx-react");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var locale_1 = require("app/locale");
var CursorGuideHandler = tslib_1.__importStar(require("./cursorGuideHandler"));
var DividerHandlerManager = tslib_1.__importStar(require("./dividerHandlerManager"));
var dragManager_1 = tslib_1.__importDefault(require("./dragManager"));
var header_1 = tslib_1.__importDefault(require("./header"));
var ScrollbarManager = tslib_1.__importStar(require("./scrollbarManager"));
var spanTree_1 = tslib_1.__importDefault(require("./spanTree"));
var utils_1 = require("./utils");
var TraceView = /** @class */ (function (_super) {
    tslib_1.__extends(TraceView, _super);
    function TraceView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = react_1.createRef();
        _this.virtualScrollBarContainerRef = react_1.createRef();
        _this.minimapInteractiveRef = react_1.createRef();
        _this.renderHeader = function (dragProps) { return (<mobx_react_1.Observer>
      {function () {
                var waterfallModel = _this.props.waterfallModel;
                return (<header_1.default organization={_this.props.organization} minimapInteractiveRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={waterfallModel.parsedTrace} event={waterfallModel.event} virtualScrollBarContainerRef={_this.virtualScrollBarContainerRef} operationNameFilters={waterfallModel.operationNameFilters}/>);
            }}
    </mobx_react_1.Observer>); };
        return _this;
    }
    TraceView.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, waterfallModel = _a.waterfallModel;
        if (!utils_1.getTraceContext(waterfallModel.event)) {
            return (<emptyStateWarning_1.default>
          <p>{locale_1.t('There is no trace for this transaction')}</p>
        </emptyStateWarning_1.default>);
        }
        return (<dragManager_1.default interactiveLayerRef={this.minimapInteractiveRef}>
        {function (dragProps) { return (<mobx_react_1.Observer>
            {function () {
                    var parsedTrace = waterfallModel.parsedTrace;
                    return (<CursorGuideHandler.Provider interactiveLayerRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={parsedTrace}>
                  <DividerHandlerManager.Provider interactiveLayerRef={_this.traceViewRef}>
                    <DividerHandlerManager.Consumer>
                      {function (dividerHandlerChildrenProps) {
                            return (<ScrollbarManager.Provider dividerPosition={dividerHandlerChildrenProps.dividerPosition} interactiveLayerRef={_this.virtualScrollBarContainerRef} dragProps={dragProps}>
                            {_this.renderHeader(dragProps)}
                            <mobx_react_1.Observer>
                              {function () {
                                    return (<spanTree_1.default traceViewRef={_this.traceViewRef} dragProps={dragProps} organization={organization} waterfallModel={waterfallModel} filterSpans={waterfallModel.filterSpans} spans={waterfallModel.getWaterfall({
                                            viewStart: dragProps.viewWindowStart,
                                            viewEnd: dragProps.viewWindowEnd,
                                        })}/>);
                                }}
                            </mobx_react_1.Observer>
                          </ScrollbarManager.Provider>);
                        }}
                    </DividerHandlerManager.Consumer>
                  </DividerHandlerManager.Provider>
                </CursorGuideHandler.Provider>);
                }}
          </mobx_react_1.Observer>); }}
      </dragManager_1.default>);
    };
    return TraceView;
}(react_1.PureComponent));
exports.default = TraceView;
//# sourceMappingURL=traceView.jsx.map