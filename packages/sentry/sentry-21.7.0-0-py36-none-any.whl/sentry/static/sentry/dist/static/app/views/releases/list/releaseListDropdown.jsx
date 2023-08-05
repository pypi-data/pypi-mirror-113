Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var ReleaseListDropdown = function (_a) {
    var _b;
    var prefix = _a.label, options = _a.options, selected = _a.selected, onSelect = _a.onSelect, className = _a.className;
    var optionEntries = Object.entries(options);
    var selectedLabel = (_b = optionEntries.find(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], _value = _b[1];
        return key === selected;
    })) === null || _b === void 0 ? void 0 : _b[1];
    return (<dropdownControl_1.default buttonProps={{ prefix: prefix }} label={selectedLabel} className={className}>
      {optionEntries.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], label = _b[1];
            return (<dropdownControl_1.DropdownItem key={key} onSelect={onSelect} eventKey={key} isActive={selected === key}>
          {label}
        </dropdownControl_1.DropdownItem>);
        })}
    </dropdownControl_1.default>);
};
exports.default = ReleaseListDropdown;
//# sourceMappingURL=releaseListDropdown.jsx.map