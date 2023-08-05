Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var jsonViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/jsonViewer"));
var panelAlert_1 = tslib_1.__importDefault(require("app/components/panels/panelAlert"));
var locale_1 = require("app/locale");
var RRWebJsonViewer = /** @class */ (function (_super) {
    tslib_1.__extends(RRWebJsonViewer, _super);
    function RRWebJsonViewer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showRawJson: false,
        };
        return _this;
    }
    RRWebJsonViewer.prototype.render = function () {
        var _this = this;
        var showRawJson = this.state.showRawJson;
        return (<react_1.Fragment>
        <StyledPanelAlert border={showRawJson} type="info">
          {locale_1.tct('This is an attachment containing a session replay. [replayLink:View the replay] or [jsonLink:view the raw JSON].', {
                replayLink: <a href="#context-replay"/>,
                jsonLink: (<a onClick={function () {
                        return _this.setState(function (state) { return ({
                            showRawJson: !state.showRawJson,
                        }); });
                    }}/>),
            })}
        </StyledPanelAlert>
        {showRawJson && <jsonViewer_1.default {...this.props}/>}
      </react_1.Fragment>);
    };
    return RRWebJsonViewer;
}(react_1.Component));
exports.default = RRWebJsonViewer;
var StyledPanelAlert = styled_1.default(panelAlert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  border-bottom: ", ";\n"], ["\n  margin: 0;\n  border-bottom: ", ";\n"])), function (p) { return (p.border ? "1px solid " + p.theme.border : null); });
var templateObject_1;
//# sourceMappingURL=rrwebJsonViewer.jsx.map