Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
function DeleteActionButton(props) {
    var handleClick = function (e) {
        var triggerIndex = props.triggerIndex, index = props.index, onClick = props.onClick;
        onClick(triggerIndex, index, e);
    };
    return (<button_1.default type="button" size="small" icon={<icons_1.IconDelete size="xs"/>} aria-label={locale_1.t('Remove action')} {...props} onClick={handleClick}/>);
}
exports.default = DeleteActionButton;
//# sourceMappingURL=deleteActionButton.jsx.map