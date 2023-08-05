Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var icons_1 = require("app/icons");
var fileExtension_1 = require("app/utils/fileExtension");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var FileIcon = function (_a) {
    var _b;
    var fileName = _a.fileName, _c = _a.size, providedSize = _c === void 0 ? 'sm' : _c, className = _a.className;
    var fileExtension = fileExtension_1.getFileExtension(fileName);
    var iconName = fileExtension ? fileExtension_1.fileExtensionToPlatform(fileExtension) : null;
    var size = (_b = theme_1.default.iconSizes[providedSize]) !== null && _b !== void 0 ? _b : providedSize;
    if (!iconName) {
        return <icons_1.IconFile size={size} className={className}/>;
    }
    return (<img src={require("platformicons/svg/" + iconName + ".svg")} width={size} height={size} className={className}/>);
};
exports.default = FileIcon;
//# sourceMappingURL=fileIcon.jsx.map