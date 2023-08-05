Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var modalManager_1 = tslib_1.__importDefault(require("./modalManager"));
var Edit = /** @class */ (function (_super) {
    tslib_1.__extends(Edit, _super);
    function Edit() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Edit.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { values: {
                name: this.props.relay.name,
                publicKey: this.props.relay.publicKey,
                description: this.props.relay.description || '',
            }, disables: { publicKey: true } });
    };
    Edit.prototype.getTitle = function () {
        return locale_1.t('Edit Key');
    };
    Edit.prototype.getData = function () {
        var savedRelays = this.props.savedRelays;
        var updatedRelay = this.state.values;
        var trustedRelays = savedRelays.map(function (relay) {
            if (relay.publicKey === updatedRelay.publicKey) {
                return updatedRelay;
            }
            return relay;
        });
        return { trustedRelays: trustedRelays };
    };
    return Edit;
}(modalManager_1.default));
exports.default = Edit;
//# sourceMappingURL=edit.jsx.map