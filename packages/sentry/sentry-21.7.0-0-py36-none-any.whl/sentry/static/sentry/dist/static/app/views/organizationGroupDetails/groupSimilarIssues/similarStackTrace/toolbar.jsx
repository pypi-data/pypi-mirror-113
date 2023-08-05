Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var toolbarHeader_1 = tslib_1.__importDefault(require("app/components/toolbarHeader"));
var locale_1 = require("app/locale");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var initialState = {
    mergeCount: 0,
};
var SimilarToolbar = /** @class */ (function (_super) {
    tslib_1.__extends(SimilarToolbar, _super);
    function SimilarToolbar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.onGroupChange = function (_a) {
            var mergeList = _a.mergeList;
            if (!(mergeList === null || mergeList === void 0 ? void 0 : mergeList.length)) {
                return;
            }
            if (mergeList.length !== _this.state.mergeCount) {
                _this.setState({ mergeCount: mergeList.length });
            }
        };
        _this.listener = groupingStore_1.default.listen(_this.onGroupChange, undefined);
        return _this;
    }
    SimilarToolbar.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    SimilarToolbar.prototype.render = function () {
        var _a = this.props, onMerge = _a.onMerge, v2 = _a.v2;
        var mergeCount = this.state.mergeCount;
        return (<panels_1.PanelHeader hasButtons>
        <confirm_1.default data-test-id="merge" disabled={mergeCount === 0} message={locale_1.t('Are you sure you want to merge these issues?')} onConfirm={onMerge}>
          <button_1.default size="small" title={locale_1.t('Merging %s issues', mergeCount)}>
            {locale_1.t('Merge %s', "(" + (mergeCount || 0) + ")")}
          </button_1.default>
        </confirm_1.default>

        <Columns>
          <StyledToolbarHeader>{locale_1.t('Events')}</StyledToolbarHeader>

          {v2 ? (<StyledToolbarHeader>{locale_1.t('Score')}</StyledToolbarHeader>) : (<react_1.Fragment>
              <StyledToolbarHeader>{locale_1.t('Exception')}</StyledToolbarHeader>
              <StyledToolbarHeader>{locale_1.t('Message')}</StyledToolbarHeader>
            </react_1.Fragment>)}
        </Columns>
      </panels_1.PanelHeader>);
    };
    return SimilarToolbar;
}(react_1.Component));
exports.default = SimilarToolbar;
var Columns = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"])));
var StyledToolbarHeader = styled_1.default(toolbarHeader_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=toolbar.jsx.map