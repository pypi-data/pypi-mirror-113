Object.defineProperty(exports, "__esModule", { value: true });
exports.OPEN_DELAY = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_popper_1 = require("react-popper");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var constants_1 = require("app/constants");
var domId_1 = require("app/utils/domId");
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
exports.OPEN_DELAY = 50;
/**
 * How long to wait before closing the tooltip when isHoverable is set
 */
var CLOSE_DELAY = 50;
/**
 * Used to compute the transform origin to give the scale-down micro-animation
 * a pleasant feeling. Without this the animation can feel somewhat 'wrong'.
 */
function computeOriginFromArrow(placement, arrowProps) {
    // XXX: Bottom means the arrow will be pointing up
    switch (placement) {
        case 'top':
            return { originX: arrowProps.style.left + "px", originY: '100%' };
        case 'bottom':
            return { originX: arrowProps.style.left + "px", originY: 0 };
        case 'left':
            return { originX: '100%', originY: arrowProps.style.top + "px" };
        case 'right':
            return { originX: 0, originY: arrowProps.style.top + "px" };
        default:
            return { originX: "50%", originY: '100%' };
    }
}
var Tooltip = /** @class */ (function (_super) {
    tslib_1.__extends(Tooltip, _super);
    function Tooltip() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
            usesGlobalPortal: true,
        };
        _this.tooltipId = domId_1.domId('tooltip-');
        _this.delayTimeout = null;
        _this.delayHideTimeout = null;
        _this.getPortal = memoize_1.default(function (usesGlobalPortal) {
            if (usesGlobalPortal) {
                var portal_1 = document.getElementById('tooltip-portal');
                if (!portal_1) {
                    portal_1 = document.createElement('div');
                    portal_1.setAttribute('id', 'tooltip-portal');
                    document.body.appendChild(portal_1);
                }
                return portal_1;
            }
            var portal = document.createElement('div');
            document.body.appendChild(portal);
            return portal;
        });
        _this.setOpen = function () {
            _this.setState({ isOpen: true });
        };
        _this.setClose = function () {
            _this.setState({ isOpen: false });
        };
        _this.handleOpen = function () {
            var delay = _this.props.delay;
            if (_this.delayHideTimeout) {
                window.clearTimeout(_this.delayHideTimeout);
                _this.delayHideTimeout = null;
            }
            if (delay === 0) {
                _this.setOpen();
                return;
            }
            _this.delayTimeout = window.setTimeout(_this.setOpen, delay !== null && delay !== void 0 ? delay : exports.OPEN_DELAY);
        };
        _this.handleClose = function () {
            var isHoverable = _this.props.isHoverable;
            if (_this.delayTimeout) {
                window.clearTimeout(_this.delayTimeout);
                _this.delayTimeout = null;
            }
            if (isHoverable) {
                _this.delayHideTimeout = window.setTimeout(_this.setClose, CLOSE_DELAY);
            }
            else {
                _this.setClose();
            }
        };
        return _this;
    }
    Tooltip.prototype.componentDidMount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var TooltipStore;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!constants_1.IS_ACCEPTANCE_TEST) return [3 /*break*/, 2];
                        return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/stores/tooltipStore')); })];
                    case 1:
                        TooltipStore = (_a.sent()).default;
                        TooltipStore.addTooltip(this);
                        _a.label = 2;
                    case 2: return [2 /*return*/];
                }
            });
        });
    };
    Tooltip.prototype.componentWillUnmount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var usesGlobalPortal, TooltipStore;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        usesGlobalPortal = this.state.usesGlobalPortal;
                        if (!constants_1.IS_ACCEPTANCE_TEST) return [3 /*break*/, 2];
                        return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/stores/tooltipStore')); })];
                    case 1:
                        TooltipStore = (_a.sent()).default;
                        TooltipStore.removeTooltip(this);
                        _a.label = 2;
                    case 2:
                        if (!usesGlobalPortal) {
                            document.body.removeChild(this.getPortal(usesGlobalPortal));
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    Tooltip.prototype.renderTrigger = function (children, ref) {
        var propList = {
            'aria-describedby': this.tooltipId,
            onFocus: this.handleOpen,
            onBlur: this.handleClose,
            onMouseEnter: this.handleOpen,
            onMouseLeave: this.handleClose,
        };
        // Use the `type` property of the react instance to detect whether we
        // have a basic element (type=string) or a class/function component (type=function or object)
        // Because we can't rely on the child element implementing forwardRefs we wrap
        // it with a span tag so that popper has ref
        if (React.isValidElement(children) &&
            (this.props.skipWrapper || typeof children.type === 'string')) {
            // Basic DOM nodes can be cloned and have more props applied.
            return React.cloneElement(children, tslib_1.__assign(tslib_1.__assign({}, propList), { ref: ref }));
        }
        propList.containerDisplayMode = this.props.containerDisplayMode;
        return (<Container {...propList} className={this.props.className} ref={ref}>
        {children}
      </Container>);
    };
    Tooltip.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, forceShow = _a.forceShow, children = _a.children, title = _a.title, position = _a.position, popperStyle = _a.popperStyle, isHoverable = _a.isHoverable;
        var _b = this.state, isOpen = _b.isOpen, usesGlobalPortal = _b.usesGlobalPortal;
        if (disabled) {
            return children;
        }
        var modifiers = {
            hide: { enabled: false },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
            applyStyle: {
                gpuAcceleration: true,
            },
        };
        var visible = forceShow || isOpen;
        var tip = visible ? (<react_popper_1.Popper placement={position} modifiers={modifiers}>
        {function (_a) {
                var _b;
                var ref = _a.ref, style = _a.style, placement = _a.placement, arrowProps = _a.arrowProps;
                return (<PositionWrapper style={style}>
            <TooltipContent id={_this.tooltipId} initial={{ opacity: 0 }} animate={{
                        opacity: 1,
                        scale: 1,
                        transition: testableTransition_1.default({
                            type: 'linear',
                            ease: [0.5, 1, 0.89, 1],
                            duration: 0.2,
                        }),
                    }} exit={{
                        opacity: 0,
                        scale: 0.95,
                        transition: testableTransition_1.default({ type: 'spring', delay: 0.1 }),
                    }} style={computeOriginFromArrow(position, arrowProps)} transition={{ duration: 0.2 }} className="tooltip-content" aria-hidden={!visible} ref={ref} hide={!title} data-placement={placement} popperStyle={popperStyle} onMouseEnter={function () { return isHoverable && _this.handleOpen(); }} onMouseLeave={function () { return isHoverable && _this.handleClose(); }}>
              {title}
              <TooltipArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style} background={((_b = popperStyle) === null || _b === void 0 ? void 0 : _b.background) || '#000'}/>
            </TooltipContent>
          </PositionWrapper>);
            }}
      </react_popper_1.Popper>) : null;
        return (<react_popper_1.Manager>
        <react_popper_1.Reference>{function (_a) {
            var ref = _a.ref;
            return _this.renderTrigger(children, ref);
        }}</react_popper_1.Reference>
        {react_dom_1.default.createPortal(<framer_motion_1.AnimatePresence>{tip}</framer_motion_1.AnimatePresence>, this.getPortal(usesGlobalPortal))}
      </react_popper_1.Manager>);
    };
    Tooltip.defaultProps = {
        position: 'top',
        containerDisplayMode: 'inline-block',
    };
    return Tooltip;
}(React.Component));
// Using an inline-block solves the container being smaller
// than the elements it is wrapping
var Container = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  max-width: 100%;\n"], ["\n  ", ";\n  max-width: 100%;\n"])), function (p) { return p.containerDisplayMode && "display: " + p.containerDisplayMode; });
var PositionWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.tooltip; });
var TooltipContent = styled_1.default(framer_motion_1.motion.div)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  will-change: transform, opacity;\n  position: relative;\n  color: ", ";\n  background: #000;\n  opacity: 0.9;\n  padding: 5px 10px;\n  border-radius: ", ";\n  overflow-wrap: break-word;\n  max-width: 225px;\n\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1.4;\n\n  margin: 6px;\n  text-align: center;\n  ", ";\n  ", ";\n"], ["\n  will-change: transform, opacity;\n  position: relative;\n  color: ", ";\n  background: #000;\n  opacity: 0.9;\n  padding: 5px 10px;\n  border-radius: ", ";\n  overflow-wrap: break-word;\n  max-width: 225px;\n\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1.4;\n\n  margin: 6px;\n  text-align: center;\n  ", ";\n  ", ";\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.popperStyle; }, function (p) { return p.hide && "display: none"; });
var TooltipArrow = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  width: 10px;\n  height: 5px;\n\n  &[data-placement*='bottom'] {\n    top: 0;\n    left: 0;\n    margin-top: -5px;\n    &::before {\n      border-width: 0 5px 5px 5px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n\n  &[data-placement*='top'] {\n    bottom: 0;\n    left: 0;\n    margin-bottom: -5px;\n    &::before {\n      border-width: 5px 5px 0 5px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &[data-placement*='right'] {\n    left: 0;\n    margin-left: -5px;\n    &::before {\n      border-width: 5px 5px 5px 0;\n      border-color: transparent ", " transparent transparent;\n    }\n  }\n\n  &[data-placement*='left'] {\n    right: 0;\n    margin-right: -5px;\n    &::before {\n      border-width: 5px 0 5px 5px;\n      border-color: transparent transparent transparent ", ";\n    }\n  }\n\n  &::before {\n    content: '';\n    margin: auto;\n    display: block;\n    width: 0;\n    height: 0;\n    border-style: solid;\n  }\n"], ["\n  position: absolute;\n  width: 10px;\n  height: 5px;\n\n  &[data-placement*='bottom'] {\n    top: 0;\n    left: 0;\n    margin-top: -5px;\n    &::before {\n      border-width: 0 5px 5px 5px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n\n  &[data-placement*='top'] {\n    bottom: 0;\n    left: 0;\n    margin-bottom: -5px;\n    &::before {\n      border-width: 5px 5px 0 5px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &[data-placement*='right'] {\n    left: 0;\n    margin-left: -5px;\n    &::before {\n      border-width: 5px 5px 5px 0;\n      border-color: transparent ", " transparent transparent;\n    }\n  }\n\n  &[data-placement*='left'] {\n    right: 0;\n    margin-right: -5px;\n    &::before {\n      border-width: 5px 0 5px 5px;\n      border-color: transparent transparent transparent ", ";\n    }\n  }\n\n  &::before {\n    content: '';\n    margin: auto;\n    display: block;\n    width: 0;\n    height: 0;\n    border-style: solid;\n  }\n"])), function (p) { return p.background; }, function (p) { return p.background; }, function (p) { return p.background; }, function (p) { return p.background; });
exports.default = Tooltip;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=tooltip.jsx.map