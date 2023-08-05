Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var framer_motion_1 = require("framer-motion");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var Toast = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  padding: 0 15px 0 10px;\n  margin-top: 15px;\n  background: ", ";\n  color: #fff;\n  border-radius: 44px 7px 7px 44px;\n  box-shadow: 0 4px 12px 0 rgba(47, 40, 55, 0.16);\n  position: relative;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  padding: 0 15px 0 10px;\n  margin-top: 15px;\n  background: ", ";\n  color: #fff;\n  border-radius: 44px 7px 7px 44px;\n  box-shadow: 0 4px 12px 0 rgba(47, 40, 55, 0.16);\n  position: relative;\n"])), function (p) { return p.theme.gray500; });
Toast.defaultProps = {
    initial: {
        opacity: 0,
        y: 70,
    },
    animate: {
        opacity: 1,
        y: 0,
    },
    exit: {
        opacity: 0,
        y: 70,
    },
    transition: testableTransition_1.default({
        type: 'spring',
        stiffness: 450,
        damping: 25,
    }),
};
var Icon = styled_1.default('div', { shouldForwardProp: function (p) { return p !== 'type'; } })(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  svg {\n    display: block;\n  }\n\n  color: ", ";\n"], ["\n  margin-right: ", ";\n  svg {\n    display: block;\n  }\n\n  color: ", ";\n"])), space_1.default(0.75), function (p) { return (p.type === 'success' ? p.theme.green300 : p.theme.red300); });
var Message = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Undo = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  padding-left: ", ";\n  margin-left: ", ";\n  border-left: 1px solid ", ";\n  cursor: pointer;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: inline-block;\n  color: ", ";\n  padding-left: ", ";\n  margin-left: ", ";\n  border-left: 1px solid ", ";\n  cursor: pointer;\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space_1.default(2), space_1.default(2), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var StyledLoadingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  .loading-indicator {\n    border-color: ", ";\n    border-left-color: ", ";\n  }\n"], ["\n  .loading-indicator {\n    border-color: ", ";\n    border-left-color: ", ";\n  }\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.purple300; });
function ToastIndicator(_a) {
    var indicator = _a.indicator, onDismiss = _a.onDismiss, className = _a.className, props = tslib_1.__rest(_a, ["indicator", "onDismiss", "className"]);
    var icon;
    var options = indicator.options, message = indicator.message, type = indicator.type;
    var _b = options || {}, undo = _b.undo, disableDismiss = _b.disableDismiss;
    var showUndo = typeof undo === 'function';
    var handleClick = function (e) {
        if (disableDismiss) {
            return;
        }
        if (typeof onDismiss === 'function') {
            onDismiss(indicator, e);
        }
    };
    if (type === 'success') {
        icon = <icons_1.IconCheckmark size="lg" isCircled/>;
    }
    else if (type === 'error') {
        icon = <icons_1.IconClose size="lg" isCircled/>;
    }
    // TODO(billy): Remove ref- className after removing usage from getsentry
    return (<Toast onClick={handleClick} data-test-id={type ? "toast-" + type : 'toast'} className={classnames_1.default(className, 'ref-toast', "ref-" + type)} {...props}>
      {type === 'loading' ? (<StyledLoadingIndicator mini/>) : (<Icon type={type}>{icon}</Icon>)}
      <Message>{message}</Message>
      {showUndo && <Undo onClick={undo}>{locale_1.t('Undo')}</Undo>}
    </Toast>);
}
exports.default = ToastIndicator;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=toastIndicator.jsx.map