public static function resizeMultiCamTaskImage($destination_path, $image_name, $task, $view_num, $gabarit = 'normal') {
    $crop_config_name   = $gabarit == 'grand' ? 'multicam_vu_crop_config' : 'multicam_crop_config';
    $client_crop_config = UsersConfig::where('client_id', $task->client_id)
        ->where('name', $crop_config_name)
        ->first();
    $sizes   = Config::get('image.videos_images_sizes');
    $quality = Config::get('image.quality');
    $rotate_config = Config::get('camera_rotate');

    if (($gabarit === 'grand' && isset($rotate_config[$view_num]))) {
        $image = Image::make($destination_path . $image_name);
        $image->rotate($rotate_config[$view_num]);
        $image->save();
    }

    // Get image sizes from Config
    foreach ($sizes as $size) {
        $target_dir = $destination_path . $size['width'];

        // If directory does not exists => create it
        // Dirname corespond to the "name" key of the image_size array
        if (! File::isDirectory($target_dir)) {
            File::makeDirectory($target_dir);
        }

        $image = Image::make($destination_path . $image_name);

        // Resize
        $image->resize($size['width'], null, function($constraint) {
            $constraint->aspectRatio();
            $constraint->upsize();
        });

        // Apply crop
        if ($client_crop_config && ! env('DISABLE_MULTI_CAM_AUTO_CROP', false)) {
            $crop_config_array = unserialize($client_crop_config->value);
            $crop_config = $crop_config_array["view$view_num"];
            $crop_horizontal = floor($image->width() * $crop_config['width'] / 100);
            $crop_vertical = floor($image->height() * $crop_config['height'] / 100);
            $x = floor($image->width() * $crop_config['pos_x'] / 100);
            $y = floor($image->height() * $crop_config['pos_y'] / 100);
            $image->crop($crop_horizontal, $crop_vertical, $x, $y);
        }

        // Save image to memory stream
        $stream = ImageStream::make($image->encode(null, $quality));

        // Write the memory stream to file
        $resized_name = $target_dir . '/' . $image_name;
        file_put_contents($resized_name, $stream->getContents());
    }

    // Resize the original image and save to memory stream
    $image = Image::make($destination_path . $image_name);
    $image->resize(3860, null, function($constraint) {
        $constraint->aspectRatio();
        $constraint->upsize();
    });
    $stream = ImageStream::make($image->encode(null, 100));

    // Write the memory stream to file
    file_put_contents($destination_path . $image_name, $stream->getContents());
}