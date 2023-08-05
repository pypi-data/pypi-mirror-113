Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var modalActions_1 = tslib_1.__importDefault(require("app/actions/modalActions"));
var storeConfig = {
    init: function () {
        this.reset();
        this.listenTo(modalActions_1.default.closeModal, this.onCloseModal);
        this.listenTo(modalActions_1.default.openModal, this.onOpenModal);
    },
    get: function () {
        return this.state;
    },
    reset: function () {
        this.state = {
            renderer: null,
            options: {},
        };
    },
    onCloseModal: function () {
        this.reset();
        this.trigger(this.state);
    },
    onOpenModal: function (renderer, options) {
        this.state = { renderer: renderer, options: options };
        this.trigger(this.state);
    },
};
var ModalStore = reflux_1.default.createStore(storeConfig);
exports.default = ModalStore;
//# sourceMappingURL=modalStore.jsx.map