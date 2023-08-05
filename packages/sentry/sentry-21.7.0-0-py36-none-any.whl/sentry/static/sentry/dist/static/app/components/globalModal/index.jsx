Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var focus_trap_1 = require("focus-trap");
var framer_motion_1 = require("framer-motion");
var modal_1 = require("app/actionCreators/modal");
var constants_1 = require("app/constants");
var modalStore_1 = tslib_1.__importDefault(require("app/stores/modalStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getModalPortal_1 = tslib_1.__importDefault(require("app/utils/getModalPortal"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var components_1 = require("./components");
function GlobalModal(_a) {
    var _b;
    var _c = _a.visible, visible = _c === void 0 ? false : _c, _d = _a.options, options = _d === void 0 ? {} : _d, children = _a.children, onClose = _a.onClose;
    var closeModal = React.useCallback(function () {
        var _a;
        // Option close callback, from the thing which opened the modal
        (_a = options.onClose) === null || _a === void 0 ? void 0 : _a.call(options);
        // Action creator, actually closes the modal
        modal_1.closeModal();
        // GlobalModal onClose prop callback
        onClose === null || onClose === void 0 ? void 0 : onClose();
    }, [options]);
    var handleEscapeClose = React.useCallback(function (e) { return e.key === 'Escape' && closeModal(); }, [closeModal]);
    var portal = getModalPortal_1.default();
    var focusTrap = React.useRef();
    // SentryApp might be missing on tests
    if (window.SentryApp) {
        window.SentryApp.modalFocusTrap = focusTrap;
    }
    React.useEffect(function () {
        focusTrap.current = focus_trap_1.createFocusTrap(portal, {
            preventScroll: true,
            escapeDeactivates: false,
            fallbackFocus: portal,
        });
    }, [portal]);
    React.useEffect(function () {
        var _a;
        var body = document.querySelector('body');
        var root = document.getElementById(constants_1.ROOT_ELEMENT);
        if (!body || !root) {
            return function () { return void 0; };
        }
        var reset = function () {
            var _a;
            body.style.removeProperty('overflow');
            root.removeAttribute('aria-hidden');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.deactivate();
            portal.removeEventListener('keydown', handleEscapeClose);
        };
        if (visible) {
            body.style.overflow = 'hidden';
            root.setAttribute('aria-hidden', 'true');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.activate();
            portal.addEventListener('keydown', handleEscapeClose);
        }
        else {
            reset();
        }
        return reset;
    }, [portal, handleEscapeClose, visible]);
    var renderedChild = children === null || children === void 0 ? void 0 : children({
        CloseButton: components_1.makeCloseButton(closeModal),
        Header: components_1.makeClosableHeader(closeModal),
        Body: components_1.ModalBody,
        Footer: components_1.ModalFooter,
        closeModal: closeModal,
    });
    // Default to enabled backdrop
    var backdrop = (_b = options.backdrop) !== null && _b !== void 0 ? _b : true;
    // Only close when we directly click outside of the modal.
    var containerRef = React.useRef(null);
    var clickClose = function (e) {
        return containerRef.current === e.target && closeModal();
    };
    return react_dom_1.default.createPortal(<React.Fragment>
      <Backdrop style={backdrop && visible ? { opacity: 0.5, pointerEvents: 'auto' } : {}}/>
      <Container ref={containerRef} style={{ pointerEvents: visible ? 'auto' : 'none' }} onClick={backdrop === true ? clickClose : undefined}>
        <framer_motion_1.AnimatePresence>
          {visible && (<Modal role="dialog" css={options.modalCss}>
              <Content role="document">{renderedChild}</Content>
            </Modal>)}
        </framer_motion_1.AnimatePresence>
      </Container>
    </React.Fragment>, portal);
}
var fullPageCss = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"], ["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"])));
var Backdrop = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  background: ", ";\n  will-change: opacity;\n  transition: opacity 200ms;\n  pointer-events: none;\n  opacity: 0;\n"], ["\n  ", ";\n  z-index: ", ";\n  background: ", ";\n  will-change: opacity;\n  transition: opacity 200ms;\n  pointer-events: none;\n  opacity: 0;\n"])), fullPageCss, function (p) { return p.theme.zIndex.modal; }, function (p) { return p.theme.gray500; });
var Container = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  overflow-y: auto;\n"], ["\n  ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  overflow-y: auto;\n"])), fullPageCss, function (p) { return p.theme.zIndex.modal; });
var Modal = styled_1.default(framer_motion_1.motion.div)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 640px;\n  pointer-events: auto;\n  padding: 80px ", " ", " ", ";\n"], ["\n  width: 640px;\n  pointer-events: auto;\n  padding: 80px ", " ", " ", ";\n"])), space_1.default(2), space_1.default(4), space_1.default(2));
Modal.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 15 },
    transition: testableTransition_1.default({
        opacity: { duration: 0.2 },
        y: { duration: 0.25 },
    }),
};
var Content = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  background: ", ";\n  border-radius: 8px;\n  border: ", ";\n  box-shadow: ", ";\n"], ["\n  padding: ", ";\n  background: ", ";\n  border-radius: 8px;\n  border: ", ";\n  box-shadow: ", ";\n"])), space_1.default(4), function (p) { return p.theme.background; }, function (p) { return p.theme.modalBorder; }, function (p) { return p.theme.modalBoxShadow; });
var GlobalModalContainer = /** @class */ (function (_super) {
    tslib_1.__extends(GlobalModalContainer, _super);
    function GlobalModalContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            modalStore: modalStore_1.default.get(),
        };
        _this.unlistener = modalStore_1.default.listen(function (modalStore) { return _this.setState({ modalStore: modalStore }); }, undefined);
        return _this;
    }
    GlobalModalContainer.prototype.componentDidMount = function () {
        // Listen for route changes so we can dismiss modal
        this.unlistenBrowserHistory = react_router_1.browserHistory.listen(function () { return modal_1.closeModal(); });
    };
    GlobalModalContainer.prototype.componentWillUnmount = function () {
        var _a, _b;
        (_a = this.unlistenBrowserHistory) === null || _a === void 0 ? void 0 : _a.call(this);
        (_b = this.unlistener) === null || _b === void 0 ? void 0 : _b.call(this);
    };
    GlobalModalContainer.prototype.render = function () {
        var modalStore = this.state.modalStore;
        var visible = !!modalStore && typeof modalStore.renderer === 'function';
        return (<GlobalModal {...this.props} {...modalStore} visible={visible}>
        {visible ? modalStore.renderer : null}
      </GlobalModal>);
    };
    return GlobalModalContainer;
}(React.Component));
exports.default = GlobalModalContainer;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map