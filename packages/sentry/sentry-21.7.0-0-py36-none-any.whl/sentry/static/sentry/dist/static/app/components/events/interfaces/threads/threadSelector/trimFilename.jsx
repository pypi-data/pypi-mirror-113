Object.defineProperty(exports, "__esModule", { value: true });
function trimFilename(filename) {
    var pieces = filename.split(/\//g);
    return pieces[pieces.length - 1];
}
exports.default = trimFilename;
//# sourceMappingURL=trimFilename.jsx.map